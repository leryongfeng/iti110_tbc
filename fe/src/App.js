import React, { Component } from 'react';
import styles from './App.css';
import TransactionImageUploader from './TransactionImageUploader';
import CalibrateImageUploader from './CalibrateImageUploader';

const API_URL = process.env.REACT_APP_API_URL;

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      transaction: [],
      imageUrl: null,
      logs: [],
    };

    this.startTransaction = this.startTransaction.bind(this);
    this.completeTransaction = this.completeTransaction.bind(this);
    this.getTransaction = this.getTransaction.bind(this);
    this.setImageUrl = this.setImageUrl.bind(this);
    this.addLog = this.addLog.bind(this);
  }

  addLog(message) {
    this.setState((prevState) => ({
      logs: [...prevState.logs, `${new Date().toLocaleTimeString()}: ${message}`]
    }));
  }

  startTransaction() {
    fetch(`${API_URL}/start_transaction`, {
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept' },

    })
    .then(response => response.json())
    .then(json => {
      this.setState({ transaction: json })
      this.addLog("Transaction started " + json.transaction_number)
    })
    .catch(error => this.addLog(`Start transaction failed: ${error.message}`));
  }

  completeTransaction() {
    fetch(`${API_URL}/complete_transaction`, {
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept' },
      body: JSON.stringify({ "transaction_number": this.state.transaction?.transaction_number })
    })
    .then(response => response.json())
    .then(json => {
      this.setState({ transaction: {} });
      this.addLog("Transaction completed " + json.transaction_number + ". " + json.message)
    })
    .catch(error => console.error("Fetch error:", error));
  }

  getTransaction() {
    fetch(`${API_URL}/get_transaction`, {
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept' },
      body: JSON.stringify({ "transaction_number": this.state.transaction?.transaction_number })
    })
    .then(response => response.json())
    .then(json => this.setState({ transaction: json }))
    .catch(error => console.error("Fetch error:", error));
  }

  setImageUrl(url) {
    this.setState({ imageUrl: url });
  }

  render() {
    const { transaction, imageUrl, logs } = this.state;

    return (
      <div className="container" style={{ width: "100vw", height: "100vh", padding: "20px" }}>
        <div className="jumbotron">
          <h1 className="display-4">ITI110 DEMO : FRUITS BASKET</h1>
        </div>

        <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "space-between", gap: "2px", width: "100%", height: "70vh" }}>
          {/* Left Side - Camera Card */}
          <div className="card" style={{ height: "100%", width: "48%", display: "flex", flexDirection: "column", margin: "0" }}>
            <div className="card-header">Camera (Demo)</div>
            <div className="card-body" style={{ flex: 1, padding: "10px" }}>
              <TransactionImageUploader 
                transactionNumber={transaction?.transaction_number}
                updateTransaction={this.getTransaction}
                setImageUrl={this.setImageUrl}
                addLog={this.addLog}
                />
              <CalibrateImageUploader 
                setImageUrl={this.setImageUrl} 
                addLog={this.addLog}
                />
              {/* Display uploaded image */}
              {imageUrl && (
                <div style={{ marginTop: "10px" }}>
                  <p>Uploaded Image:</p>
                  <img src={imageUrl} alt="Uploaded Preview" style={{ width: "100%", maxHeight: "200px", objectFit: "cover" }} />
                </div>
              )}
            </div>
          </div>

          {/* Right Side - Two Cards Stacked Vertically */}
          <div style={{ display: "flex", flexDirection: "column", width: "48%", height: "100%" }}>
            
            {/* Transaction Items Card */}
            <div className="card" style={{ flex: 1, width: "100%", marginBottom: "10px" }}>
              <div className="card-header">Items</div>
              <div className="card-body" style={{ maxHeight: "200px", overflowY: "auto", padding: "10px" }}>
                {transaction?.items?.length > 0 ? (
                  transaction.items.map((item, index) => (
                    <p key={index} style={{ margin: "0", padding: "2px 0" }}>
                      {item.item_name} - ${item.item_price.toFixed(2)}
                    </p>
                  ))
                ) : (
                  <p>No items available</p>
                )}
              </div>
            </div>

            {/* Logs Card */}
            <div className="card" style={{ flex: 1, width: "100%" }}>
              <div className="card-header">Logs</div>
              <div className="card-body" style={{ maxHeight: "200px", overflowY: "auto", padding: "10px" }}>
                {logs.map((log, index) => (
                  <p key={index} style={{ margin: "0", padding: "2px 0" }}>
                    {log}
                  </p>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div style={{ display: "flex", justifyContent: "space-between", padding: "10px" }}>
          <button className="btn btn-primary" onClick={this.startTransaction}>Start Transaction</button>
          <p className="card-text" style={{ margin: "auto" }}>Transaction ID: {transaction?.transaction_number}</p>
          <button className="btn btn-primary" onClick={this.completeTransaction}>Complete Transaction</button>
        </div>
      </div>
    );
  }
}

export default App;
