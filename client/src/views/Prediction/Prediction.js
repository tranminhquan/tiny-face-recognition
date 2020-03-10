import React, { Component, lazy, Suspense } from 'react';
import { Bar, Line } from 'react-chartjs-2';
import ImageUploader from 'react-images-upload';

import { CustomTooltips } from '@coreui/coreui-plugin-chartjs-custom-tooltips';
import { getStyle, hexToRgba } from '@coreui/coreui/dist/js/coreui-utilities'

import {
    Badge,
    Button,
    ButtonDropdown,
    ButtonGroup,
    ButtonToolbar,
    Card,
    CardBody,
    CardFooter,
    CardHeader,
    CardTitle,
    Col,
    Dropdown,
    DropdownItem,
    DropdownMenu,
    DropdownToggle,
    Progress,
    Row,
    Table,
    CardGroup,
  } from 'reactstrap';

import axios from 'axios';
const Widget06 = lazy(() => import('../../views/Widgets/Widget06'));

const brandPrimary = getStyle('--primary');
const brandSuccess = getStyle('--success');
const brandInfo = getStyle('--info');
const brandWarning = getStyle('--warning');
const brandDanger = getStyle('--danger');


// Data variables
var fomular_info = [{
    r: null,
    alpha: null,
    beta: null,
    gamma: null,
    delta: null,
    e_s: null,
    e_b: null,
}]

// Card chart dataset (historgram of data)
var dataset_info = {
    dataset_id: "ORL",
    n_data: 400,
}

var cardChartData = {
    labels: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    datasets: [
      {
        label: 'My First dataset',
        backgroundColor: 'rgba(255,255,255,.3)',
        borderColor: 'transparent',
        data: [78, 81, 80, 45, 34, 12, 40, 75, 34, 89, 32, 68, 54, 72, 18, 98],
      },
    ],
  };


var training_info = {
    epochs: 100,
    acc: [],
    val_acc: [],
    loss: [],
    val_loss: [],
}

const cardChartOpts = {
    tooltips: {
      enabled: false,
      custom: CustomTooltips
    },
    maintainAspectRatio: false,
    legend: {
      display: false,
    },
    scales: {
      xAxes: [
        {
          display: false,
          barPercentage: 0.6,
        }],
      yAxes: [
        {
          display: false,
        }],
    },
  };

  var trainingChart = {
    labels: [...Array(100).keys()],
    datasets: [
      {
        label: 'Accuracy',
        backgroundColor: hexToRgba(brandInfo, 10),
        borderColor: brandInfo,
        pointHoverBackgroundColor: '#fff',
        borderWidth: 2,
        data: training_info.acc,
      },
      {
        label: 'Validation Accuracy',
        backgroundColor: 'transparent',
        borderColor: brandSuccess,
        pointHoverBackgroundColor: '#fff',
        borderWidth: 2,
        data: training_info.val_acc,
      },
      {
        label: 'Loss',
        backgroundColor: 'transparent',
        borderColor: brandDanger,
        pointHoverBackgroundColor: '#fff',
        borderWidth: 1,
        borderDash: [8, 5],
        data: training_info.loss,
      },
      {
        label: 'Validation Loss',
        backgroundColor: 'transparent',
        borderColor: brandWarning,
        pointHoverBackgroundColor: '#fff',
        borderWidth: 1,
        borderDash: [8, 5],
        data: training_info.val_loss,
      },
    ],
  };
  
  const trainingChartOpts = {
    tooltips: {
      enabled: false,
      custom: CustomTooltips,
      intersect: true,
      mode: 'index',
      position: 'nearest',
      callbacks: {
        labelColor: function(tooltipItem, chart) {
          return { backgroundColor: chart.data.datasets[tooltipItem.datasetIndex].borderColor }
        }
      }
    },
    maintainAspectRatio: false,
    legend: {
      display: false,
    },
    scales: {
      xAxes: [
        {
          gridLines: {
            drawOnChartArea: false,
          },
          ticks: {
            beginAtZero: true,
            // maxTicksLimit: 5,
            // stepSize: Math.ceil(250 / 5),
            max: 100,
          },
        }],
      yAxes: [
        {
          ticks: {
            beginAtZero: true,
            maxTicksLimit: 5,
            // stepSize: Math.ceil(250 / 5),
            max: 1,
          },
        }],
    },
    elements: {
      point: {
        radius: 0,
        hitRadius: 10,
        hoverRadius: 4,
        hoverBorderWidth: 3,
      },
    },
  };

class Prediction extends Component {
    constructor(props){
        super(props);

        this.state ={
            selected_info: 0,
            fomular_info: fomular_info,
            dataset_info: [{dataset_id: null, n_data: null}],
            training_info: training_info,
            images: null,
            predict_data: 
                {
                    training_info: {loss: [], val_loss: [], acc: [], val_acc: []},
                    predictions: [
                        {
                            method: {label:0, accuracy: 0},
                            nb: {label:null, accuracy: null},
                            bilinear: {label:null, accuracy: null},
                            bicubic: {label:null, accuracy: null},
                        }]
                },
            training_chart: trainingChart,
            predict_image_urls: [],
            interpolate_image_urls: [],
            image_size: "M x N",
            model_size: "M x N"
        };

        // this.fileChangedHandler = this.fileChangedHandler.bind(this);
        this.uploadHandler = this.uploadHandler.bind(this);
        // this.componentDidMount = this.componentDidMount.bind(this);
        // this.onClickItemDropDown = this.onClickItemDropDown(this);
    };

   

    fileChangedHandler = (e) => {

        this.setState({images: e.target.files});

        // const files = e.target.files;  
        
        // this.setState({image: URL.createObjectURL(e.target.files[0])});
        
        // if (files.length === 0)
        //     return false;
        // const form = new FormData();

        // for (const file of files){
        //     form.append('images', file, file.name)
        // }

        // axios.post('http://localhost:5000/predict', form);
    };

    uploadHandler() {
 
    };

    onClickPredict = () => {
        if (this.state.images.length === 0)
            return false;
        
        const form = new FormData();

        for (const file of this.state.images){
            form.append('images', file, file.name);
            
        }

        form.set('r', this.state.fomular_info[this.state.selected_info].r);
        form.set('alpha', this.state.fomular_info[this.state.selected_info].alpha);
        form.set('beta', this.state.fomular_info[this.state.selected_info].beta);
        form.set('gamma', this.state.fomular_info[this.state.selected_info].gamma);
        form.set('delta', this.state.fomular_info[this.state.selected_info].delta);
        form.set('e_s', this.state.fomular_info[this.state.selected_info].e_s);
        form.set('e_b', this.state.fomular_info[this.state.selected_info].e_b);
        form.set('dataset_id', this.state.dataset_info[this.state.selected_info].dataset_id);

        console.log(form);
        axios.post('http://localhost:5000/predict', form)
        .then((response) => {
            console.log(response);
            console.log(response.data.training_info);

            this.setState({predict_data: response.data});
            var _chart = this.state.training_chart;

            _chart.datasets[0].data = response.data.training_info.acc;
            _chart.datasets[1].data = response.data.training_info.val_acc;
            _chart.datasets[2].data = response.data.training_info.loss;
            _chart.datasets[3].data = response.data.training_info.val_loss;

            this.setState({training_chart: _chart}, ()=>{
                console.log(this.state.training_chart);
            });

            this.setState({predict_image_urls: response.data.image_urls}, ()=>{
                console.log(this.state.predict_image_urls[0]);
            });

            this.setState({interpolate_image_urls: response.data.interpolate_image_urls}, () =>{
                console.log(this.state.interpolate_image_urls);
            });

            this.setState({image_size: response.data.image_size}, () =>{
                console.log(this.state.image_size);
            });

            this.setState({model_size: response.data.model_size}, () =>{
                console.log(this.state.model_size);
            });
            // var bla = JSON.parse(response.data);
            // console.log(bla);
            // console.log(bla.training_info);
            // this.setState({predict_data: bla}, () => {
            //     console.log(this.state.predict_data);
            //     console.log((JSON.parse(this.state.predict_data)).training_info);
            // });
            // console.log(response);
            // console.log(bla);
            // console.log(JSON.stringify(bla.training_info));
            // console.log(JSON.parse(JSON.stringify(response.data.predictions)));
        });
    }
       
    componentDidMount = () =>{
        // this.setState({dataset_info: [{dataset_id: null, n_data: null}]});
        // var temp = this;
        axios.get('http://localhost:5000/predict').
        then((response) => {
            var dt_data = JSON.parse(response.data.dataset_info);
            var f_data = JSON.parse(response.data.fomular_info);
            this.setState({dataset_info: dt_data, fomular_info: f_data});
            console.log(this.state.dataset_info);
            console.log(this.state.fomular_info);
            
        }).catch((error) => {
            // handle error
            console.log(error);
          });
    }

    onClickItemDropDown = (index) => {
        this.setState({selected_info: index});
        console.log(index);

        // send dataset_id to server to get training info
        // console.log(this.state.dataset_info[this.state.selected_info]);
        // axios.get('http://localhost:5000/training?dataset_id=' + this.state.dataset_info[this.state.selected_info].dataset_id)

        // .then((response) => {
        //     console.log(response)

        //     console.log(response.data.fomular_info)
        // });
    }

    render() {
        return (
            <div className="animated fadeIn">
                <Row>
                    <Col xs="12" sm="4" lg="4">
                        <Card className="text-black" >
                            <Row>
                                <Col sm="4">
                                    <CardTitle className="m-2">Upload image</CardTitle>
                                </Col>
                                <Col sm="8">
                                    <input type="file" onChange={this.fileChangedHandler}
                                />
                                </Col>
                            </Row>

                            <Row>
                                <Col>
                                    <Button block color="primary" onClick={this.onClickPredict}>Predict</Button>
                                </Col>
                                
                            </Row>

                            <Row>
                                <Col>
                                    <img src={this.state.predict_image_urls[0]}></img>
                                </Col>

                                
                            </Row>
                            
                        </Card>
                    </Col>

                    <Col xs="12" sm="4" lg="4">
                        <Card className="text-white bg-primary">
                        
                        <CardBody className="pb-0">
                            <ButtonGroup className="float-right">
                                <ButtonDropdown id='card4' isOpen={this.state.card4} toggle={() => { this.setState({ card4: !this.state.card4 }); }}>
                                    <DropdownToggle caret className="p-0" color="transparent">
                                    <i className="icon-settings"></i>
                                    </DropdownToggle>
                                    <DropdownMenu right>
                                        {this.state.dataset_info.map((f_value, index) => (
                                            <DropdownItem key={index} onClick={()=>this.onClickItemDropDown(index)}>{f_value.dataset_id}</DropdownItem>
                                        ))}
                                    </DropdownMenu>
                                </ButtonDropdown>
                            </ButtonGroup>
                            <div className="text-value">{this.state.dataset_info[this.state.selected_info].dataset_id}</div>
                            <div>{this.state.dataset_info[this.state.selected_info].n_data} images</div>
                        </CardBody>
                        <div className="chart-wrapper mx-3" style={{ height: '70px' }}>
                            <Bar data={cardChartData} options={cardChartOpts} height={70} />
                        </div>
                        </Card>
                    </Col>

                    <Col xs="12" sm="4" lg="4">
                        <Card className="text-white bg-primary">
                        <Row>
                            <Col>
                                <div className="text-value mb-2 mt-4 ml-3">Fomular</div>
                            </Col>
                            <Col>
                            </Col>
                        </Row>
 
                        <CardBody className="brand-card-body">
                        
                            <div>
                                <div className="text-value">{this.state.fomular_info[this.state.selected_info].alpha}</div>
                                <div className="text-uppercase text-muted small">alpha</div>
                            </div>
                            <div>
                                <div className="text-value">{this.state.fomular_info[this.state.selected_info].beta}</div>
                                <div className="text-uppercase text-muted small">beta</div>
                            </div>
                            <div>
                                <div className="text-value">{this.state.fomular_info[this.state.selected_info].gamma}</div>
                                <div className="text-uppercase text-muted small">gamma</div>
                            </div>
                            <div>
                                <div className="text-value">{this.state.fomular_info[this.state.selected_info].delta}</div>
                                <div className="text-uppercase text-muted small">delta</div>
                            </div>
                        
                            <div>
                                <div className="text-value">{this.state.fomular_info[this.state.selected_info].e_s}</div>
                                <div className="text-uppercase text-muted small">e_s</div>
                            </div>
                            <div>
                                <div className="text-value">{this.state.fomular_info[this.state.selected_info].e_b}</div>
                                <div className="text-uppercase text-muted small">e_b</div>
                            </div>
                        
                        </CardBody>
                       
                        </Card>
                    </Col>
                </Row>

                <Row>
                    <Col>
                        <Card>
                        <CardHeader>
                            <Row className="text-center">
                            <Col sm={12} md className="mb-sm-2 mb-0">
                                <div className="text-muted">Label</div>
                                <strong>{this.state.predict_data.predictions[0].method.label}</strong>
                            </Col>
                            <Col sm={12} md className="mb-sm-2 mb-0 d-md-down-none">
                                <div className="text-muted">Probability</div>
                                <strong>{this.state.predict_data.predictions[0].method.accuracy}</strong>
                            </Col>     
                            <Col sm={12} md className="mb-sm-2 mb-0">
                                <div className="text-muted">Input image size</div>
                                <strong>{this.state.image_size}</strong>
                            </Col>
                            <Col sm={12} md className="mb-sm-2 mb-0">
                                <div className="text-muted">Image size of model</div>
                                <strong>{this.state.model_size}</strong>
                            </Col>
                            {/* <Col sm={12} md className="mb-sm-2 mb-0">
                                <div className="text-muted">Blocks</div>
                                <strong>3</strong>
                            </Col>
                            <Col sm={12} md className="mb-sm-2 mb-0 d-md-down-none">
                                <div className="text-muted">Average accuracy</div>
                                <strong>90 %</strong>
                            </Col> */}
                            </Row>
                        </CardHeader>
                        <CardBody>
                            <Row>
                            <Col sm="5">
                                <CardTitle className="mb-0">Training and prediction</CardTitle>
                            </Col>
                           
                            </Row>
                            <div className="chart-wrapper" >
                            <Line data={this.state.training_chart}  />
                            </div>
                        </CardBody>

                        </Card>
                    </Col>
                </Row>

                <CardGroup className="mb-4">
                    <Widget06 img={this.state.predict_image_urls[0]} color="danger" 
                            label={this.state.predict_data.predictions[0].method.label} 
                            value={this.state.predict_data.predictions[0].method.accuracy*100}>Proposed method</Widget06>
                    <Widget06 img={this.state.interpolate_image_urls[3*0 + 0]} color="info" 
                            label={this.state.predict_data.predictions[0].nb.label} 
                            value={this.state.predict_data.predictions[0].nb.accuracy*100}>Nearest Neighbour</Widget06>
                    <Widget06 img={this.state.interpolate_image_urls[3*0 + 1]} color="success" 
                            label={this.state.predict_data.predictions[0].bilinear.label} 
                            value={this.state.predict_data.predictions[0].bilinear.accuracy*100}>Bilinear</Widget06>
                    <Widget06 img={this.state.interpolate_image_urls[3*0 + 2]} color="warning" 
                            label={this.state.predict_data.predictions[0].bicubic.label} 
                            value={this.state.predict_data.predictions[0].bicubic.accuracy*100}>Bicubic</Widget06>
                </CardGroup>

                {/* <Row>
                    <Col>
                        <Card>
                        <CardHeader>
                            Traffic {' & '} Sales
                        </CardHeader>
                        <CardBody>
                            <Row>
                                <Col sm="2">
                                    <div className="callout callout-info">
                                    <small className="text-muted">Nearest Neighbour</small>
                                    <br />
                                    <strong className="h4">{this.state.predict_data.predictions[0].nb.label}</strong>
                                    <br />
                                    <strong className="h4">{this.state.predict_data.predictions[0].nb.accuracy}</strong>
                                    </div>
                                </Col>

                                <Col sm="2">
                                    <div className="callout callout-info">
                                    <small className="text-muted">Bilinear</small>
                                    <br />
                                    <strong className="h4">{this.state.predict_data.predictions[0].bilinear.label}</strong>
                                    <br />
                                    <strong className="h4">{this.state.predict_data.predictions[0].bilinear.accuracy}</strong>
                                    </div>
                                </Col>

                                <Col sm="2">
                                    <div className="callout callout-info">
                                    <small className="text-muted">Bicubic</small>
                                    <br />
                                    <strong className="h4">{this.state.predict_data.predictions[0].bicubic.label}</strong>
                                    <br />
                                    <strong className="h4">{this.state.predict_data.predictions[0].bicubic.accuracy}</strong>
                                    </div>
                                </Col>
                            </Row>
                            <Row>
                                <Col>               
                                <div className="progress-group mb-4">
                                <div className="progress-group-prepend">
                                    <span className="progress-group-text">
                                    Nearest Neighbour
                                    </span>
                                </div>
                                <div className="progress-group-bars">
                                    <Progress className="progress-xs" color="info" value="34" />
                                </div>
                                </div>
                                <div className="progress-group mb-4">
                                <div className="progress-group-prepend">
                                    <span className="progress-group-text">
                                    Bilinear
                                    </span>
                                </div>
                                <div className="progress-group-bars">
                                    <Progress className="progress-xs" color="info" value="56" />
                                </div>

                                </div>
                                <div className="progress-group mb-4">
                                <div className="progress-group-prepend">
                                    <span className="progress-group-text">
                                    Bicubic
                                    </span>
                                </div>
                                <div className="progress-group-bars">
                                    <Progress className="progress-xs" color="info" value="12"/>
                                    
                                </div>

                                </div>
                                
                                <div className="legend text-center">
                                <small>
                                    <sup className="px-1"><Badge pill color="info">&nbsp;</Badge></sup>
                                    Accuracy
                                    &nbsp;
                                  
                                </small>
                                </div>
                            </Col>
                            </Row>
                        </CardBody>
                        </Card>
                    </Col>
                </Row> */}
            
            </div>
        );
    }
}

export default Prediction