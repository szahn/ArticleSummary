import React = require("react");

class SummarySentence extends React.Component<any, any>{
    componentDidMount(props: any){
        this.props = props;
    }
    
    render(){
        return (<li>{this.props.sentence}</li>);
    }
}

export = SummarySentence;