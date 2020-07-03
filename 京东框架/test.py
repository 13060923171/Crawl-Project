import requests
import json
url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=12611705,12660454,12610002,64397711026,12669803,24675618191,12598158,12675942,69543169703,12241204,69257978102,12622435,31373896774,12445029,29308861250,12585016,12375644,37830680848,12052200,12346637,12661197,11748995,12397576,12660458,11487324,12701880,68665370422,12613720,12513593,69004796494,12509944&callback=jQuery5999681&_=1593412248445'
headers = {
    "Cookie": "unpl=V2_ZzNtbRAEQxYiDBNTKR1cAmIGEg1KVEYVcgxFBH4ZCQIyABpbclRCFnQUR1NnGlQUZwEZWUtcQRdFCEdkeB5fA2AFEFlBZxVLK14bADlNDEY1WnwHBAJfF3ILQFJ8HlQMZAEUbXJUQyV1CXZdeR1aB2QHE1tyZ0QlRThGXXMbXQZXAiJcchUXSXEKQVVzGBEMZQcUX0FTQhNFCXZX; __jdv=76161171|google-search|t_262767352_googlesearch|cpc|kwd-362776698237_0_cb12f5d6c516441a9241652a41d6d297|1593410310158; __jdu=835732507; areaId=19; ipLoc-djd=19-1601-50256-0; PCSYCityID=CN_440000_440100_440114; shshshfpa=b3947298-5c63-ba93-8e7d-b89e3e422382-1593410312; shshshfpb=eVvsT1HAgXe1EsnsQQ6HTpQ%3D%3D; __jdc=122270672; shshshfp=158c0090e5888d932458419e12bac1d7; 3AB9D23F7A4B3C9B=VLVTNQOO6BLWETXYSO5XADLGXR7OIDM3NHDDPRNYKWBPH45RRTYXIJNGG5TFHJ5YYFBFDEARKUWAM3XO4ZWTNCDX7U; shshshsID=86f31dd02161606d1c9bf211a7b066fd_1_1593415724113; __jda=122270672.835732507.1593410309.1593410310.1593415724.2; __jdb=122270672.1.835732507|2.1593415724; JSESSIONID=F5D0DC3E7CDA9CFFAA42F672B5826835.s1; jwotest_product=99",
    "Host": "club.jd.com",
    "Referer": "https://item.jd.com/12611705.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}
# html = requests.get(url,headers=headers)
# json_decode = html.text
# start = json_decode.find('{"CommentsCount":')
# end = json_decode.find('PoorRateStyle":1}]}')+len('PoorRateStyle":1}]}')
# results = json.loads(json_decode[start:end])
# for result in results['CommentsCount']:
#     print(result['CommentCount'])
url2= 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=12611705&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1'
html = requests.get(url2,headers= headers)
json_decode = html.text
start = json_decode.find('{"productAttr"')
end = json_decode.find('"afterDays":0}]}')+len('"afterDays":0}]}')
results = json.loads(json_decode[start:end])
for result in results['comments']:
    print(result["content"])

