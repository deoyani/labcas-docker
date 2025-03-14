const express = require('express');
const app = express();

app.get('/sso/saml/login', (req, res) => {
  const redirectTo = req.query.redirectTo || 'http://localhost:3000';
  // In a real scenario you'd handle authentication logic here.
  // For the mock, just redirect:
  res.redirect(redirectTo);
});

app.get('/sso/auth/_tokeninfo', (req, res) => {
  res.json({
    userDetails: {
      userId: 'testUser',
      userEmail: 'user@example.com',
      userName: 'Test',
      userLastName: 'User',
      winId: 'test1',
      Group: 'Mock Auth Group'
    },
    token: 'dummy-jwt-token-value'
  });
});

app.listen(3001, () => {
  console.log('Mock auth service running on port 3001');
});
