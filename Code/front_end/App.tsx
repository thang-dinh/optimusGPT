//App.tsx

import React, { useEffect, useState, createContext, useContext } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider, AuthProviderProps, useAuth } from 'react-oidc-context';
import { User, WebStorageStateStore } from 'oidc-client-ts';


// TO BE CONTD. OTHER DETAILS NECESSARY FOR APP.TSX