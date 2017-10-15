import React, { Component } from 'react';
import { connect } from 'react-redux';
import { reduxForm, Field, Form } from 'redux-form';
import * as actions from '../../actions/auth';

const renderInput = field => {
    const { input, type } = field;
    return (
        <div>
            <input {...input} type={type} className="form-control" />
        </div>
    );
}

class Signin extends Component {
    handleFormSubmit({ username, password }) {
        var username = this.refs.username.value;
        var password = this.refs.password.value;
        console.log(username, password);
        this.props.signinUser({ username, password });
    }

    renderAlert() {
        const { errorMessage } = this.props;
        if (errorMessage) {
            return (
                <div className="alert alert-danger">
                    <strong>Oops!</strong>{errorMessage}
                </div>
            );
        }
    }

    render () {
		/* props from reduxForm */
		const { handleSubmit, fields: { username, password }} = this.props;
		/* console.log(...username);*/
		return (
			<form onSubmit={handleSubmit(this.handleFormSubmit.bind(this))}>
			<fieldset className="form-group">
				<label>Username:</label>
                <input type="text" className="form-control" id="username" ref="username"/>
			</fieldset>
			<fieldset className="form-group">
				<label>Password:</label>
				<input type="password" className="form-control" id="password" ref="password" />
			</fieldset>
			{this.renderAlert()}
			<button action="submit" className="btn btn-primary">Sign in</button>
			</form>
		);
    }
}

function mapStateToProps(state) {
    return { 
        // form: state.form,
        errorMessage: state.auth.error
     };
}

Signin = reduxForm({ form: 'signin', fields: [ 'username', 'password' ] })(Signin);

export default connect(mapStateToProps, actions)(Signin);