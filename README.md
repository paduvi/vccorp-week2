# Phan Đức Việt - Thực tập VCCorp tuần 2
Báo cáo thực tập VCCorp tuần 2: ElasticSearch, Naive Bayes và K-Means

### ElasticSearch:
- ElasticSearch là 1 Database với khả năng full-text search cực kỳ tốt, thiết kế dựa trên Apache Lucene search. Nó có thể lưu trữ dữ liệu lên tới hàng tỉ record, mà tốc độ query vẫn được đảm bảo gần như Real-time.
- Get record theo id:
```
es.get(index='posts', doc_type='blog', id=2)
```
- Search:

  - Dùng cú pháp của Lucene:
  ```
es.search(index='posts', q='author:"Benjamin Pollack"')
es.search(index='posts', q='Santa')
es.search(index='posts', q='author:"Benjamin Pollack" python')
  ```

  - Sử dụng build-in option (`match`):
  
  ```
  es.search(index="sw", body={"query": {"match": {'name':'Darth Vader'}}})
  ```

  - Tiền tố (`prefix`):
  ```
  es.search(index="sw", body={"query": {"prefix" : { "name" : "lu" }}})
  ```

  - Từ khóa `like`:
  ```
  es.search(index="sw", body={"query": {"multi_match": 
                             {"fields": ["name"], "query": "jaba", "fuzziness": "AUTO"}}})
  ```
 
  - ...
