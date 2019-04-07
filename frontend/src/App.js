import React, { Component } from 'react';
import './App.css';
import axios from "axios";

class App extends Component {

	constructor(props) {
		super(props);
		this.handleOnClickCrawl = this.handleOnClickCrawl.bind(this);
		this.state = {
			url: '',
			depth: '',
			endpoint : 'http://localhost:8000/crawler?format=json',
			crawledData: [],
			error : false,
		}
	}

	handleOnClickCrawl(e) {
		e.preventDefault();
		this.setState({ crawledData: [], error : 0 });
		if (this.depth.value !== ''  && this.url.value !== '') {
			try {
				axios
					.get( this.state.endpoint + "&depth=" + this.depth.value + "&url=" + this.url.value )
					.then(res => this.setState({ crawledData: res.data }))
					.catch(err => console.log(err));

			} catch (e) {
				console.log(e);
			}
		} else {
			this.setState({ error: true });
		}
	}

	render() {

		var crawled = [];
		var iserror = "";

		if( 0 < this.state.crawledData.length) {
			crawled = this.state.crawledData.map(item => (
					<React.Fragment key={item.id}>
					<dt>{item.url}</dt>
					{item.images.map((image,index)=>(
						<img key={index} className ="img-thumbnail img-fluid" src={image} alt="img"/>
					))}
					</React.Fragment>
				)) ;
		}

		if( this.state.error ) {
			iserror = <div className="text-danger">
						Please enter valid input
					</div>
		}

		return (
			<div className="container">
				<br/>

				<div className ="form-group col-md-4">
					{iserror}
					<input type="text"
						className ="form-control"
						id="url"
						placeholder="Seed URL"
						ref={(input) => { this.url = input; }} />
				</div>
				<div className ="form-group col-md-4">
					<input
						type="number"
						className ="form-control"
						id="depth"
						placeholder="Depth to Crawl"
						ref={(input) => { this.depth = input; }} />
				</div>
				<div className ="form-group col-md-4">
					<button type="submit" className ="btn btn-primary" onClick={this.handleOnClickCrawl}>Crawl</button>
				</div>

				<div className = "container">
					{crawled}
				</div>

			</div>
		);
	}
}

export default App;