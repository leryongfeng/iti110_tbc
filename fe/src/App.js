import React, { Component } from 'react';
import styles from './App.css'

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      posts: []
    }
  }

  // on mount do call -- shouldnt be needed for the demo app
  // componentDidMount() {
  //   const url = "https://jsonplaceholder.typicode.com/posts";
  //   fetch(url)
  //   .then(response => response.json())
  //   .then(json => this.setState({ posts: json }))
  // }

  getPosts() {
    const url = "https://jsonplaceholder.typicode.com/posts";
    fetch(url)
    .then(response => response.json())
    .then(json => this.setState({ posts: json }))
  }

  render() {
    const { posts } = this.state;

    return (
      <div className="container">
        <div class="jumbotron">
          <h1 class="display-4">ITI110 DEMO : FRUITS BASKET</h1>
        </div>

        <div className="card">
          <div className="card-header">
            Featured
          </div>
          <div className="card-body">
            <h5 className="card-title">Special title treatment</h5>
            <p className="card-text">With supporting text below as a natural lead-in to additional content.</p>
          <a href="#" className="btn btn-primary" onClick={()=>this.getPosts()}>Get Posts</a>
          </div>
        </div>

        <div style={{ display: "flex", flexWrap: "wrap" }}>
          {posts.map((post) => (
            <div className="card" key={post.id}>
              <div className="card-header">
                #{post.id} {post.title}
              </div>
              <div className="card-body">
                <p className="card-text">{post.body}</p>
              </div>
            </div>
          ))}
        </div>

      </div>
    );
  }
}
export default App;
