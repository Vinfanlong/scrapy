import scrapy
import json
from urllib.parse import quote
from playwright.sync_api import sync_playwright


class NikeSpider(scrapy.Spider):
    name = "nike"
    allowed_domains = ["nike.com.cn"]
    start_urls = "https://api.nike.com.cn/cic/browse/v2"
    query_params = {
        'queryid': 'products',
        'anonymousId': 'undefined',
        'country': 'cn',
        'endpoint': quote('/product_feed/rollup_threads/v2?filter=marketplace(CN)&filter=language(zh-Hans)&filter=employeePrice(true)&anchor=0&consumerChannelId=d9a5bc42-4b9c-4976-858a-f159cf99c647&count=24'),
        'language': 'zh-Hans',
        'localizedRangeStr': quote('{lowestPrice} — {highestPrice}')
    }

    def start_requests(self):
        # 构造完整的API请求URL
        api_url = f"{self.start_urls}?{'&'.join([f'{k}={v}' for k,v in self.query_params.items()])}"
        
        # 添加必要的请求头
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.nike.com.cn/'
        }
        
        yield scrapy.Request(
            url=api_url,
            headers=headers,
            callback=self.parse_api
        )
    
    def parse_api(self, response):
        try:
            data = json.loads(response.text)
            products = data.get('data', {}).get('products', {}).get('products', [])
            
            for product in products:
                product_data = {
                    'title': product.get('title', '') + ' ' + product.get("subtitle", ''),
                    'price': product.get('price', {}).get("currentPrice", ''),
                    'color': product.get('colorways', [{}])[0].get("colorDescription", ""),
                    'size': '',  # 初始化为空，后面会填充
                    'sku': product.get('url', '').split('/')[-1],
                    'detail': '',
                    'img_urls': product.get("images", {}).get("squarishURL", ""),
                }
                # yield scrapy.Request(
                #     url = product.get('url').replace("{countryLang}", "https://www.nike.com.cn"),
                #     headers={'Referer': 'https://www.nike.com.cn/'},
                #     meta={"playwright":True},
                #     callback=self.parse_detail,
                # )

                yield scrapy.Request(
                    url = "https://api.nike.com.cn/discover/product_details_availability/v1/marketplace/CN/language/zh-Hans/consumerChannelId/d9a5bc42-4b9c-4976-858a-f159cf99c647/groupKey/" + product.get('url').split('-')[-2].split('/')[0],
                    headers={'nike-api-caller-id':'com.nike.commerce.nikedotcom.web'},
                    meta={'products':product_data},
                    callback=self.parse_size,
                )

            # 分页处理（示例：修改anchor参数获取下一页）
            current_anchor = self.query_params['endpoint'].split('anchor%3D')[1].split('%')[0]
            next_anchor = str(int(current_anchor) + 24)
            self.query_params['endpoint'] = self.query_params['endpoint'].replace(
                'anchor%3D0', 
                'anchor%3D'+next_anchor
            )
          
            # 请求下一页
            next_page_url = f"{self.start_urls}?{'&'.join([f'{k}={v}' for k,v in self.query_params.items()])}"
            yield scrapy.Request(
                url=next_page_url,
                headers={'Referer': 'https://www.nike.com.cn/'},
                callback=self.parse_api
            )
        except Exception as e:
            self.logger.error(f"API解析失败: {e}")

    def parse_detail(self,response):
        yield {
        "dynamic_data": response.css("div.rendered-content::text").get()
    }
    

    def parse_size(self, response):
        try:
            product_data = response.meta['products'].copy()
            data = json.loads(response.text)
            products = data.get('sizes')
            size_str = ''

            for product in products:
                size_str += product.get('localizedLabel')+','
            
            product_data['size'] = size_str
            yield product_data
        
        except Exception as e:
            self.logger.error(f"size 失败: {e}")