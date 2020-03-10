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
import WebCam from 'react-webcam'
const Widget01 = lazy(() => import('../Widgets/Widget01'));


class FaceCollection extends Component{
    
    constructor(props){
        super(props);

        this.state = {
            captured_images: [],
            input_label: null,
            image_src: null,
            counter: 0,
            interval_capture: null,
            timer: null,
            timer_counter: 0,
            frame: null
        };
    };

    b64toBlob = (b64Data, contentType, sliceSize) => {
        contentType = contentType || '';
        sliceSize = sliceSize || 512;

        var byteCharacters = atob(b64Data);
        var byteArrays = [];

        for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
            var slice = byteCharacters.slice(offset, offset + sliceSize);

            var byteNumbers = new Array(slice.length);
            for (var i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }

            var byteArray = new Uint8Array(byteNumbers);

            byteArrays.push(byteArray);
        }

        var blob = new Blob(byteArrays, {type: contentType});
        return blob;
    }

    predict = () => {
        
    }
    

    setRef = webcam => {
        this.webcam = webcam;
      };

    capture = () => {
        this.state.captured_images.push(this.webcam.getScreenshot().toString());

        this.setState({image_src: this.webcam.getScreenshot()});
        this.setState({counter: this.state.counter + 1});
    }

    timerCount = () => {
        this.setState({timer_counter: this.state.timer_counter + 1});
    }
    
    startCapture = () => {
        this.setState({captured_images: []});
        this.setState({counter: 0, timer_counter: 0});

        this.setState({interval_capture: setInterval(this.capture, 50)});
        this.setState({timer: setInterval(this.timerCount, 1000)});
      };

    stopCapture = () => {
        clearInterval(this.state.interval_capture);
        clearInterval(this.state.timer);    
    }

    submitCapturedImages = () =>{
        const form = new FormData();

        for (const url of this.state.captured_images){
            var block = url.split(";");
            var contentType = block[0].split(":")[1]
            var realData = block[1].split(",")[1]

            var blob = this.b64toBlob(realData, contentType)
            console.log(blob)
            form.append('captured_images', blob);
        }
        
        form.set('label', this.state.input_label);
        // console.log(this.state.captured_images[0]);
        // console.log(this.state.input_label);
        axios.post('http://localhost:5000/dataset', form);
    }

    render(){
        const videoConstraints = {
            width: 720,
            height: 720,
            facingMode: "user"
          };
        
        return(
            <div className="animated fadeIn">
                <Row>
                    <Col xs="12" sm="4" lg="4">
                        <Card>
                            <CardBody>
                                <WebCam
                                    audio={false}
                                    height={350}
                                    ref={this.setRef}
                                    screenshotFormat="image/png"
                                    width={350}
                                    videoConstraints={videoConstraints}
                                    />
                                <Button onClick={this.startCapture}>Start capture</Button>
                                <Button onClick={this.stopCapture}>Stop</Button>

                                <Button color="primary" onClick={this.predict}>Submit for training</Button>
                                </CardBody>
                        </Card>
                    </Col>

                    <Col xs="12" sm="4" lg="4">
                        <Card>
                            <CardBody>
                                <img src={this.state.image_src} height={350} width={350}/>
                                <InputGroup>
                                    <Input placeholder="Name" value={this.state.input_label} onChange={(e) => {this.setState({input_label: e.target.value})}} />
                                </InputGroup>
                            </CardBody>
                        </Card>
                    </Col>

                    <Col xs="12" sm="4" lg="4">
                        <Row>
                            <Col>
                                <Card className="text-white bg-info">
                                    <CardBody className="pb-0">
                                        <div className="text-value">{this.state.counter}</div>
                                        <div>Number of captured images</div>

                                        <div className="text-value">{this.state.timer_counter}</div>
                                        <div>Seconds time</div>
                                    </CardBody>

                                    <CardFooter>
                                        <Button onClick={this.submitCapturedImages}> Submit </Button>
                                    </CardFooter>
                                </Card>
                            </Col>
                        </Row>

                        {/* <Row>
                            <Col>
                                <Widget01 color="primary" variant="inverse" mainText="89.9%" value="89.9" header="Label" />
                            </Col>
                        </Row> */}
                    </Col>           
                </Row>
            
            </div>
        );
    }
}

export default FaceCollection;