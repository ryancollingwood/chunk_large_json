# chunk_large_json
Chunk a single BIG json file into many smaller ones

# Overview

Say you've got a large JSON Lines document such as the example below (sourced from: [http://deepyeti.ucsd.edu/jianmo/amazon/categoryFiles/All_Amazon_Review.json.gz](http://deepyeti.ucsd.edu/jianmo/amazon/categoryFiles/All_Amazon_Review.json.gz)

For an exact definition of JSON Lines see: [https://jsonlines.org/](https://jsonlines.org/)

```
{"overall": 1.0, "verified": false, "reviewTime": "12 11, 2015", "reviewerID": "A27BTSGLXK2C5K", "asin": "B017O9P72A", "reviewerName": "Jacob M. Wessler", "reviewText": "Alexa is not able to control my lights. If I ask her to tell me what LIFX can do, she will give me an example with one of my group names. If I use that exact same group name in a new request, she'll await that she doesn't recognize the name. This skill is VERY buggy and has not yet worked for me. I even rest Alexa, uninstalled LIFX, and set everything up again.", "summary": "VERY Buggy, doesn't work.", "unixReviewTime": 1449792000}
{"overall": 4.0, "vote": "5", "verified": false, "reviewTime": "12 8, 2015", "reviewerID": "A27ZJ1NCBFP1HZ", "asin": "B017O9P72A", "reviewerName": "Greg", "reviewText": "Alexa works great for me so far, but I'm also only controlling a single bulb at the moment. Turning on/off, changing colors and adjusting brightness are all easy and quick. That being said, I'm expecting complications as I add more bulbs (hope for the best prepare for the worst, right?)\n\nI'd speculate that some other users' frustrations might stem from Alexa not recognizing their bulb or room names. After simplifying my bulb name to 'Lamp' and listing it under a Living Room group (within the LIFx app), I've been able to address it by either category pretty consistently.\n\"Turn on/off living room lights.\"\n\"Change lamp light to [color]\"\n\"Dim living room lights to [X]%\"\n\nLike any new tech, you can expect growing pains and bugs early on. Be patient. This skill isn't perfect by any means, but I'd say it's off to a decent start", "summary": "So Far So Good", "unixReviewTime": 1449532800}
{"overall": 1.0, "vote": "11", "verified": false, "reviewTime": "12 7, 2015", "reviewerID": "ACCQIOZMFN4UK", "asin": "B017O9P72A", "reviewerName": "Da-Gr8-1", "reviewText": "Weak!!\n\nAlexa doesn't even recognize the name Lifx.\nIt's a waste of time to even ask her to turn on and off lights", "summary": "Time waster", "unixReviewTime": 1449446400}
{"overall": 2.0, "verified": false, "reviewTime": "12 5, 2015", "reviewerID": "A3KUPJ396OQF78", "asin": "B017O9P72A", "reviewerName": "Larry Russlin", "reviewText": "Can only control one of two bulbs from one of two echos", "summary": "Buggy", "unixReviewTime": 1449273600}
{"overall": 1.0, "vote": "2", "verified": false, "reviewTime": "02 2, 2018", "reviewerID": "A1U1RE1ZI19E1H", "asin": "B017O9P72A", "reviewerName": "Rebekah", "reviewText": "this worked great then randomly stopped. please update.", "summary": "stopped working", "unixReviewTime": 1517529600}
{"overall": 5.0, "verified": false, "reviewTime": "01 15, 2018", "reviewerID": "A3TXR8GLKS19RE", "asin": "B017O9P72A", "reviewerName": "Nello", "reviewText": "Great skill", "summary": "Great", "unixReviewTime": 1515974400}
{"overall": 1.0, "vote": "4", "verified": false, "reviewTime": "01 5, 2018", "reviewerID": "AVIWE1LJXCG77", "asin": "B017O9P72A", "reviewerName": "Pete Johnson", "reviewText": "Pretty crappy. Won&rsquo;t connect with Alexis", "summary": "Returning to", "unixReviewTime": 1515110400}
{"overall": 1.0, "vote": "2", "verified": false, "reviewTime": "01 4, 2018", "reviewerID": "A1FOHYK23FJ6CN", "asin": "B017O9P72A", "reviewerName": "L. Ray Humphreys", "reviewText": "Not happy. Can not connect to Alexa regardless.", "summary": "Can not connect to ECHO", "unixReviewTime": 1515024000}
{"overall": 1.0, "vote": "5", "verified": false, "reviewTime": "12 30, 2017", "reviewerID": "A1RRDX9AOST1AN", "asin": "B017O9P72A", "reviewerName": "Viola", "reviewText": "Can not connect a hue lights to Alexa. Linked the LIFX in the Amazon Alexa app. Can not located the smart hue bulbs. It should not be this hard to connect to Alexa. Even watched a you tube video and still", "summary": "Connecting is a no go", "unixReviewTime": 1514592000}
{"overall": 1.0, "vote": "5", "verified": false, "reviewTime": "12 29, 2017", "reviewerID": "AA4DHYT5YSSIT", "asin": "B017O9P72A", "reviewerName": "angie anj", "reviewText": "The service works with google home, but doesn't work with alexa. I'm getting rid of the \"I'm  not sure\" machine.", "summary": "Does not work", "unixReviewTime": 1514505600}
```

And you'd like to break it into many smaller `.json` documents, then this is for you.

# Getting Up and Running

## Install Dependencies
Assuming:
* you haven't got the dependencies installed 
* you have your own virtual env setup or don't care
```
pip install -r requirements.txt
```
## Invoking the script

Assuming the source data is in a relative directory `data/` and you want to write out the many small files to `output/`
```
python chunk_large_json.py -input_file data/All_Amazon_Review.json -output_dir output
```

## Parameters

    -input_file INPUT_FILE
                        path to large JSON file
    -output_dir OUTPUT_DIR
                        Output directory where we'll write out the data.
                        Must NOT already exist e.g. output/
    -nrows [NROWS]      Number of lines to read from large JSON file. If not
                        specified all lines are used.
    -chunksize [CHUNKSIZE]
                        Process the large JSON file as separate chunks of this
                        size
    -processes [PROCESSES]
                        Number of processes to spawn to write out the chunks,
                        defaults to number of CPUs.
