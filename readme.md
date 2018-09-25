
# Presentation 1 Name Disambiguation

本项目是用来对db中的论文信息进行处理，因为同一个名字可能指代很多个人，我们需要正确的把 ta们甄别出来。数据集从dblp中下载，选取下面链接中的0001-0010 “Jun Zhang” 数据集作为你方法的测试。

### Setup and Run

```json

dblp的基本信息有：

{
    'bibsource': 'dblp computer science bibliography, https://dblp.org',
    'biburl': 'https://dblp.org/rec/bib/journals/cma/Dai0W16', 
    'timestamp': 'Sun, 28 May 2017 01:00:00 +0200', 
    'doi': '10.1016/j.camwa.2015.12.007', 
    'url': 'https://doi.org/10.1016/j.camwa.2015.12.007', 
    'year': '2016',
    'pages': '431--442', 
    'number': '1',
    'volume': '71', 
    'journal': 'Computers {\\&} Mathematics with Applications', 
    'title': 'Higher order {ADI} method with completed Richardson extrapolation\nfor solving unsteady convection-diffusion equations',
    'author': 'Ruxin Dai and\nJun Zhang and\nYin Wang', 
    'ENTRYTYPE': 'article',
    'ID': 'DBLP:journals/cma/Dai0W16'
}

```


```python

    pip3 install bibtexparser
    
    python3 main.py

```


