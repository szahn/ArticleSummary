import React = require("react");

class ArticleTitle extends React.Component<any, any>{
    componentDidMount(props: any){
        this.props = props;
    }
    
    render(){
        return (<h3 className="title">
            <a target="_blank" href={this.props.url}>{this.props.title}</a>
            </h3>);
    }
}

export = ArticleTitle;