import React = require("react");

class ArticleToggle extends React.Component<any, any>{
    
    render(){
        const classes = this.props.isCollapsed ? "glyphicon glyphicon-plus" : "glyphicon glyphicon-minus";
        return (<button onClick={this.props.onToggleClicked} type="button" className="btn btn-default toggle-btn">
                <span className={classes}></span>
            </button>);
    }
}

export = ArticleToggle;