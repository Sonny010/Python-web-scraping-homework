from lxml import etree
import requests
import os

# 爬取配置
BASE_URL = "https://books.toscrape.com/catalogue/category/books_1/page-{}.html"
HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36"
}

# 获取页面 HTML
def get_page_html(page_num):
    url = BASE_URL.format(page_num)
    response = requests.get(url, headers=HEADER)
    response.encoding = "utf-8"
    if response.status_code == 200:
        return etree.HTML(response.text)
    else:
        print(f"Failed to retrieve page {page_num}. Status code: {response.status_code}")
        return None

# 解析页面书籍信息
def parse_books(html):
    book_list = []
    if html is None:
        return book_list

    book_x_list = html.xpath('//ol/li/article[@class="product_pod"]')
    for book in book_x_list:
        books = {}

        title = book.xpath('./h3/a/@title')[0]  # 书名
        price = book.xpath("./div/p[@class='price_color']/text()")[0]  # 价格
        state = book.xpath("./div/p[@class='instock availability']/text()")[1].strip().strip('\n')

        cover = book.xpath("./div/a/img/@src")[0].strip()  # 封面路径
        cover_url = "https://books.toscrape.com/" + cover.lstrip('../')  # 拼接完整 URL

        # 存储书籍信息
        books['title'] = title
        books['price'] = price
        books['state'] = state
        books['cover_url'] = cover_url

        book_list.append(books)
    return book_list

# 下载图片
def download_image(image_url, save_path):
    try:
        response = requests.get(image_url, headers=HEADER)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to download image: {image_url}")
    except Exception as e:
        print(f"Error downloading image {image_url}: {e}")

# 主函数
def scrape_books(pages_to_scrape=1):
    all_books = []
    # 确保文件夹存在
    if not os.path.exists("./pic"):
        os.mkdir("./pic")
        print("目录创建成功")
    else:
        print("文件夹已存在")

    # 爬取多页数据
    for page_num in range(1, pages_to_scrape + 1):
        print(f"正在爬取第 {page_num} 页...")
        html = get_page_html(page_num)
        books = parse_books(html)
        all_books.extend(books)

    # 保存书籍信息
    with open('./pic/书籍信息.txt', 'w', encoding='utf-8') as f:
        f.write('序号\t书名\t价格\t状态\n')
        for index, book in enumerate(all_books, start=1):
            str1 = f"{index}\t{book['title']}\t{book['price']}\t{book['state']}\n"
            f.write(str1)

            # 保存封面图片
            safe_title = book['title'].replace(':', '-').replace('/', '-')
            image_extension = book['cover_url'].split('.')[-1]
            book_path = f"./pic/{index}.{safe_title}.{image_extension}"
            print(f"Downloading: {book_path}")
            download_image(book['cover_url'], book_path)

    print("爬取完成！")

# 执行爬取
if __name__ == "__main__":
    # 自定义要爬取的页数
    num_pages = int(input("请输入要爬取的页数: "))
    scrape_books(num_pages)
