const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const VALID_MEASURES = [
  'Violent crime rate',
  'Unemployment',
  'Children in poverty',
  'Diabetic screening',
  'Mammography screening',
  'Preventable hospital stays',
  'Uninsured',
  'Sexually transmitted infections',
  'Physical inactivity',
  'Adult obesity',
  'Premature Death',
  'Daily fine particulate matter'
];

module.exports = async function handler(req, res) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(404).json({ error: 'Not found' });
  }

  // Check content type
  if (req.headers['content-type'] !== 'application/json') {
    return res.status(400).json({ error: 'Content-Type must be application/json' });
  }

  const { zip, measure_name, coffee } = req.body;

  // Check for coffee=teapot easter egg
  if (coffee === 'teapot') {
    return res.status(418).json({ error: "I'm a teapot" });
  }

  // Validate required parameters
  if (!zip || !measure_name) {
    return res.status(400).json({ error: 'Both zip and measure_name are required' });
  }

  // Validate zip format (5 digits)
  if (!/^\d{5}$/.test(zip)) {
    return res.status(400).json({ error: 'zip must be a 5-digit number' });
  }

  // Validate measure_name
  if (!VALID_MEASURES.includes(measure_name)) {
    return res.status(400).json({ error: 'Invalid measure_name' });
  }

  try {
    const dbPath = path.join(process.cwd(), 'data.db');
    const db = new sqlite3.Database(dbPath);

    const results = await new Promise((resolve, reject) => {
      const query = `
        SELECT chr.*
        FROM county_health_rankings chr
        JOIN zip_county zc ON chr.fipscode = zc.county_code
        WHERE zc.﻿zip = ? AND chr.Measure_name = ?
      `;

      db.all(query, [zip, measure_name], (err, rows) => {
        if (err) {
          reject(err);
        } else {
          resolve(rows);
        }
      });
    });

    db.close();

    if (results.length === 0) {
      return res.status(404).json({ error: 'No data found for the given zip and measure_name' });
    }

    return res.status(200).json(results);

  } catch (error) {
    console.error('Database error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}