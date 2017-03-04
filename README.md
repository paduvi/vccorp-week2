# Phan Đức Việt - Thực tập VCCorp tuần 2
Báo cáo thực tập VCCorp tuần 2: ElasticSearch, Naive Bayes và K-Means

### ElasticSearch:
- ElasticSearch là 1 Database với khả năng full-text search cực kỳ tốt, thiết kế dựa trên Apache Lucene search. Nó có thể lưu trữ dữ liệu lên tới hàng tỉ record, mà tốc độ query vẫn được đảm bảo gần như Real-time.
- Get record theo id:
```
es.get(index='posts', doc_type='blog', id=2)
# GET /posts/blog/2
```
- Search:

  - Dùng cú pháp của Lucene:
  ```
es.search(index='posts', q='author:"Benjamin Pollack"')
# GET /posts/_search?q=author%3ABenjamin Pollack

es.search(index='posts', q='Santa')
# GET /posts/_search?q=Santa

es.search(index='posts', q='author:"Benjamin Pollack" python')
# GET /posts/_search?q=author%3ABenjamin Pollack+python

es.search(index='posts', type='blog', q='+name:(mary john) +date:>2014-09-10 +(aggregations geo)') # +:or
# GET /posts/blog/_search?q=%2Bname%3A(mary+john)+%2Bdate%3A%3E2014-09-10+%2B(aggregations+geo)
  ```

  - Sử dụng query DSL:
  
  ```
  es.search(index="sw", body={"query": {"match": {'name':'Darth Vader'}}})
  ```
  ```
  GET /sw/_search
  {
      "query": {
          "match": {
              "name": "Darth Vader"
          }
      }
  }
  ```
  ```
  es.search(index="sw", body={"query": {"prefix" : { "name" : "lu" }}})
  ```
  ```
  GET /sw/_search
  {
      "query": {
          "prefix": {
              "name": "lu"
          }
      }
  }
  ```
  ```
  es.search(index="sw", body={"query": {"multi_match": 
                             {"fields": ["name"], "query": "jaba", "fuzziness": "AUTO"}}})
  
  # range, term, terms, exists
  ```
  - Kết hợp nhiều mệnh đề:
  ```
  {
      "bool": {
          "must":     { "match": { "tweet": "elasticsearch" }},
          "must_not": { "match": { "name":  "mary" }},
          "should":   { "match": { "tweet": "full text" }},
          "filter":   { "range": { "age" : { "gt" : 30 }} }
      }
  }
  ```
  ```
  {
      "bool": {
          "must": { "match":   { "email": "business opportunity" }},
          "should": [
              { "match":       { "starred": true }},
              { "bool": {
                  "must":      { "match": { "folder": "inbox" }},
                  "must_not":  { "match": { "spam": true }}
              }}
          ],
          "minimum_should_match": 1
      }
  }
  ```
 a - `must`: bắt buộc phải match mệnh đề (có tính score)
 
 b - `must_not`: bắt buộc phải không match mệnh đề (có tính score)
 
 c - `should`: match càng nhiều mệnh đề score càng cao, tuy nhiên nếu không match thì không ảnh hưởng tới query result
 
 d - `filter`: chỉ dùng để include/exclude query result, không tác động lên score
 
- Demo Implement: bắt chước khung search trong Gmail:
 
  1. Để kiếm dữ liệu mẫu, mình sử dụng tool `gmvault`: `pip install gmvault`
  
  2. Sửa lại email trong file `ES/sync_mail.sh` rồi chạy: `./sync_mail.sh`
  
  3. Đánh index dữ liệu mail đã sync được: `./parsing-and-index-mail.py`
  
  4. Tiến hành search: `./demo-search-email.py query=vccorp`
  
  Kết quả: ![Test ElasticSearch Mail](http://i.imgur.com/gHkLf2W.png)
 
 ### Bayes:
 
 - Implement mô hình Gaussian Naive Bayes:
 ![Gaussian Naive Bayes](http://i.imgur.com/gcchE1Y.png)
 
 - Dữ liệu test: iris.txt
 - Thành phần: shuffle + 80/20 cho train/test
 - File thực thi: 
 ```
 cd NaiveBayes
 ./gaussian-naive-bayes-iris.py
 ```
 
 ![Gaussian Naive Bayes](http://i.imgur.com/JkFapIS.png)
 
 ### KMeans:
 - Demo implement: compress ảnh màu
 - File thực thi:
 ```
 cd KMeans
 ./kmeans-compressor.py
 ```
 
 Options:
 - `k`: số lượng màu sau khi xử lý (Default: 196)
 
 Kết quả: ![KMeans Picture Compress](http://i.imgur.com/ggqQGzB.png)
 
 
