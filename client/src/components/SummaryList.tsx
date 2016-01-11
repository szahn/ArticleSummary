import React = require("react");
import SummarySentence = require("./SummarySentence");

class SummaryList extends React.Component<any, any>{
    componentDidMount(props: any){
        this.props = props;
    }
    
    render(){
        const sentences = this.props.summary.map((sentence, idx)=> <SummarySentence key={idx} sentence={sentence}/>);
        return (<ol className="summary-list">{sentences}</ol>);
    }
}

export = SummaryList;