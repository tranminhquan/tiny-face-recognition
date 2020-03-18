import React, { Component, lazy, Suspense } from 'react';
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
    InputGroup,
    Input
  } from 'reactstrap';

import axios from 'axios';

class FaceRecognition extends Component{
    constructor(props){
        super(props);

        this.state = {
            frame: null,
            label: null,
            prob: null
        }
    }

    predict = () => {
        axios.post('http://localhost:5000/stream')
        .then((response) => {
            this.setState({label: response.data.label});
            this.setState({prob: response.data.prob});
        });
    }

    // startPredict = () => {
    //     setInterval(this.predict, 500);
    // }

    componentDidMount = () =>{
        // setInterval(this.predict, 500);

        // this.interval();


        // console.log('start streamming request');
        // this.setState({dataset_info: [{dataset_id: null, n_data: null}]});
        // var temp = this;
        // axios.get('http://localhost:5000/video_feed').
        // then((response) => {
        //     console.log(response.data);
        //     this.setState({frame: response.data})
            
        // }).catch((error) => {
        //     // handle error
        //     console.log(error);
        //   });
    }

    render(){
        return(
            <div className="animated fadeIn">
                <Row>
                    <Col>
                        <img src="http://celeb.kyanon.digital/stream"/>
                        <Button onClick={() => {setInterval(this.predict, 500);}}>Predict</Button>
                    </Col>

                    <Col>
                        <p>{this.state.label}</p>
                        <p>{this.state.prob}</p>
                    </Col>
                </Row>
                
            </div>
        )
    }
}

export default FaceRecognition;