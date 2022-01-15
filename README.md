# 3d_retrieval_with_pointnet

PointNet Source : https://github.com/charlesq34/pointnet

ShapeNet Data : https://shapenet.org/
<br><br>

## Train with Tensorflow Docker
Tf1.15 with Python 2
```
nvidia-docker run -v {Your Project Path}:/projects -it tensorflow/tensorflow:1.15.0-gpu
```

```
cd part_seg
python train.py
```

## How to use
Use Python3. You should have full ShapeNet Data.

### 1. extract aircrat information
```
python extract_aircraft.py
```

### 2. create json file 
`airplane_before_ontology.json` is result file.

```
python create_aircraft_json.py
```

### 3. create ontology
```
python create_aircraft_ontology.py
```

### 4. Calculate similarities
Name_all.csv is manually created dbpedia mapping data.

```
cd retrieval
python rank_similarity.py
```