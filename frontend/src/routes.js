import React from 'react';
import {Route, IndexRoute} from 'react-router';

import Main from './components/Main';

import Signin from './components/auth/signin';
import Signout from './components/auth/signout';


export default (
    <Route path="/" component={Main}>
	<Route path="login" component={Signin} />
	<Route path="logout" component={Signout} />        		
    </Route>
)
