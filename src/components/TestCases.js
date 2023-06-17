import React, { useEffect, useState } from 'react';
import socketIOClient from 'socket.io-client';
import './custom.css';

const TestCases = () => {
  // ...

  return (
    <div className="container">
      <h1 className="text-center">Test Cases</h1>
      <div className="form-group">
        <input
          type="text"
          className="form-control"
          placeholder="Search test cases..."
          value={searchTerm}
          onChange={handleSearchChange}
        />
      </div>
      <ul className="list-group">
        {filteredTestCases.map((testCase, index) => (
          <li key={index} className="list-group-item">
            <strong>Name:</strong> {testCase.name}
            <br />
            <strong>Description:</strong> {testCase.description}
            <br />
            <strong>Estimate Time:</strong> {testCase.estimate_time}
            <br />
            <strong>Module:</strong> {testCase.module}
            <br />
            <strong>Priority:</strong> {testCase.priority}
            <br />
            <label>
              <strong>Status:</strong>
              <select
                className="form-control select-status"
                value={testCase.status}
                onChange={(event) => handleStatusChange(event, index)}
              >
                <option value="Pass">Pass</option>
                <option value="Fail">Fail</option>
              </select>
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TestCases;
