const express = require('express');
const app = express();

const es = require('elasticsearch');
const esClient = new es.Client({
    host: '172.18.22.9:9210',
    log: 'trace'
});

app.listen(3000, () => console.log('listening at port 3000'));

app.use(express.static('public'));

app.get('/api', async (req, res) => {
    const payload = {
        "size": 6,
        "sort": [{
            "ts": {"order": "desc"}
        }],
        "query": {
        "match_all": {}
        }
    }
    
    const resp = await esClient.search({
        index: 'test_index',        
        body: payload
    });    

    let jsonData = {}
    
    let i;
    
    for(i=0; i<=5; i++){
        let data = (resp.hits.hits[(5-i)]._source);
        let newData = "data" + (i+1);
        
        jsonData[newData] = data;    
    };

    res.json(jsonData);   
    
});




