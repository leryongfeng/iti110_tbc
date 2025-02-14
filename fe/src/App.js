import React, { Component } from 'react';
import styles from './App.css'
import ImageUploader from './ImageUploader';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      transaction: []
    };

    this.startTransaction = this.startTransaction.bind(this);
    this.completeTransaction = this.completeTransaction.bind(this);
    this.getTransaction = this.getTransaction.bind(this);

  }

  startTransaction() {
    const url = "http://127.0.0.1:5000/start_transaction";

    fetch(url, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then(json => this.setState({ transaction: json }))
    .catch(error => console.error("Fetch error:", error));
  }

  completeTransaction() {
    const url = "http://127.0.0.1:5000/complete_transaction";

    fetch(url, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({  
        "transaction_number": this.state.transaction?.transaction_number // FIX: Ensure state exists
      })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then(json => this.setState({ transaction: json }))
    .catch(error => console.error("Fetch error:", error));
  }

  getTransaction() {
    const url = "http://127.0.0.1:5000/get_transaction";

    fetch(url, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({  
        "transaction_number": this.state.transaction?.transaction_number // FIX: Ensure state exists
      })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then(json => this.setState({ transaction: json }))
    .catch(error => console.error("Fetch error:", error));
  }

  render() {
    const { transaction } = this.state;

    return (
      <div className="container" style={{ height: "100%"}}>
        <div class="jumbotron">
          <h1 class="display-4">ITI110 DEMO : FRUITS BASKET</h1>
        </div>

        <div style={{ display: "flex", flexWrap: "wrap", flex: "1", width: "100%", height: "100%", justifyContent: "space-between"}}>
          <div className="card" style={{ height: "100%"}}>
              <div className="card-header">
                Test Card 1
              </div>
              <div className="card-body">
                <p className="card-text">Content 1</p>
              </div>
            </div>
            <div className="card">
              <div className="card-header">
                Transaction ID: #{transaction.transaction_number}
              </div>
              <div className="card-body">
                <p className="card-text">Content 2</p>
              </div>
            </div>
        </div>

        <div style={{ display: "flex", flexWrap: "wrap", flex: "1", width: "100%", height: "100%", justifyContent: "space-between"}}>
          <a href="#" className="btn btn-primary" onClick={()=>this.startTransaction()}>Start Transaction</a>
          <ImageUploader 
            transactionNumber={this.state.transaction?.transaction_number}
            updateTransaction={this.getTransaction} />
          <a href="#" className="btn btn-primary" onClick={()=>this.completeTransaction()}>Complete Transaction</a>
        </div>

      </div>
    );
  }
}
export default App;
