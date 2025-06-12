# T-prep Data Preprocessing

[**T-prep**](https://github.com/INISW-6th/t-prep)에서 사용할 데이터를 수집하고 전처리하는 프로젝트입니다.

## 설명
이 프로젝트는 수집한 데이터를 다음과 같은 과정을 거쳐 전처리합니다.

1. **미래엔 중학교 2학년 역사 교과서(교사용)**
    - '본문'과 '판서 가이드라인'을 raw 파일에서 추출한다.
    - 문서 형태의 원본 데이터를 tabular로 정형화한다`xlsx`.
    - tabular 데이터를 메타데이터를 포함하여 `json`으로 변환한다.
   
3. **미래엔 중학교 2학년 역사 지도서**
    - 문서 형태의 원본 데이터를 tabular로 정형화한다`xlsx`.
    - tabular 데이터를 메타데이터를 포함하여 `json`으로 변환한다.

4. **한국학중앙연구회 한국민족문화대백과사전**
    - 라벨링된 키워드를 민족문화대백과사전 API를 통해 검색한 결과를 크롤링한다.
    - 검색된 내용을 저장 후, tabular로 정형화한다`xlsx`.
    - tabular 데이터를 메타데이터를 포함하여 `json`으로 변환한다.

## 파일 구조
```
├── code/   # 수집 및 전처리 코드
|   ├── crawler-encykorea.ipynb
|   ├── metadata-board.ipynb
|   ├── metadata-encykorea.ipynb
|   ├── metadata-learning-way.ipynb
|   └── metadata-textbook.ipynb
├── data/   # 전처리 완료된 데이터
|   ├── board.json
|   ├── encykorea.json
|   ├── learning-way.json
|   └── textbook.json
└── raw/    # 수집한 원본 또는 정형 데이터
    ├── encykorea/ # 민족대백과 API를 통한 수집 결과
    |   ├── encykorea(1).xlsx
    |   ├── encykorea(2).xlsx
    |   ├── encykorea(3).xlsx
    |   ├── encykorea(4-1).xlsx
    |   ├── encykorea(4-2).xlsx
    |   └── encykorea(5).xlsx
    ├── board.xlsx
    ├── learning-way.xlsx
    └── textbook.xlsx
```
<!--
- code: 수집 및 전처리 코드
   - `crawler-encykorea.ipynb`
   - `metadata-board.ipynb`
   - `metadata-encykorea.ipynb`
   - `metadata-learning-way.ipynb`
   - `metadata-textbook.ipynb`    
- data: 전처리 완료된 데이터
   - `board.json`
   - `encykorea.json`
   - `learning-way.json`
   - `textbook.json` 
- raw: 원본 또는 정형 데이터
   - `encykorea.xlsx`
   - `board.xlsx`
   - `learning-way.xlsx`
   - `textbook.xlsx`
-->

## 탐색적 데이터 분석(EDA)
### encykorea
![](/src/encykorea-eda-1.png)

## 시행착오(Trial and Error)
1. 메테데이터 형식 변환
- 메타데이터의 형식과 데이터셋의 분할 단위 등에 대한 실험을 지속적으로 반복했습니다. 
- 수 차례의 실험 결과, 현재의 구조가 최적이라고 판단했으며, 시행착오의 결과물은 `/data/temp/*`에서 확인하실 수 있습니다.

2. 키워드 추출 방법 모색
- TF-IDF, NER, Key BERT 등 다양한 알고리즘을 사용해 키워드 추출을 진행했지만, 문맥이 반영되지 않아 만족스러운 결과물을 얻지 못했습니다.
- 교과서 전체 분량이 약 200~300페이지이기에, 각 주제별로 데이터 라벨링을 진행하는 것이 더 효과적이라고 판단해 수기로 키워드를 추출했습니다. 
