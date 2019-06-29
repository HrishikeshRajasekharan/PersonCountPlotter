document.addEventListener("DOMContentLoaded", function() {
    getData();
    setInterval(getData, 240000);
});


const CHART = document.getElementById("myChart");

function getData() {
    let dataA = [];
    let dataB = [];
    let dataTime = [];

    fetch('/api').then(res => res.json()).then(res => {                    
        dataA.push(res.data1.countA, res.data2.countA, res.data3.countA, res.data4.countA, res.data5.countA, res.data6.countA);
        dataB.push(res.data1.countB, res.data2.countB, res.data3.countB, res.data4.countB, res.data5.countB, res.data6.countB);
        dataTime.push(res.data1.ts, res.data2.ts, res.data3.ts, res.data4.ts, res.data5.ts, res.data6.ts);

        console.log(dataA);
        console.log(dataB);
        console.log(dataTime);
        console.log(typeof(dataTime[0]));    
    }).then(() => {
            let barChart = new Chart(CHART, {
                type: 'bar',
                data: {
                    labels: dataTime,
                    
                    datasets: [{
                        label: 'Aisle A',
                        data: dataA,
                        
                        backgroundColor: 'rgba(255, 99, 132, 0.8)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Aisle B',
                        data: dataB,
                        
                        backgroundColor: 'rgba(54, 162, 235, 0.8)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }
                    ]
                },
                options: {
                    animation: {
                        duration: 0
                    },

                    title: {
                        display: true,
                        text: 'Time Series of Person Count Data',
                        fontSize: 16
                    },
                    legend: {
                        position: 'top'
                    },
                    responsive: true,
                    tooltips: {
                        mode: 'index',
                        itemSort: function(a, b) {
                            return b.datasetIndex - a.datasetIndex
                        },
                        intersect: false
                    },
                    scales: {
                        xAxes: [{
                            
                            stacked: true,
                            scaleLabel: {
                                display: true,
                                labelString: 'Time'
                            },
                            barPercentage: 0.7,
                        }],
                        yAxes: [{
                            stacked: true,
                            scaleLabel: {
                                display: true,
                                labelString: 'Number of Persons'
                            },
                            ticks: {
                                beginAtZero: true,
                            }
                        }]
                    }
                }
            })
    });            
};






