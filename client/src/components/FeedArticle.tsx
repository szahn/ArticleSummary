import React = require("react");

class FeedArticle extends React.Component<any, any>{
    componentDidMount(props: any){
        this.props = props;
    }
    
    render(){
        const article = this.props.article;
        const summary  = article.summary.map((summ, idx)=> <li key={idx}>{summ}</li>);
        return (<section className="article"><h3 className="title"><a target="_blank" href={article.url}>{article.title}</a></h3><ul>{summary}</ul></section>);
    }
}

export = FeedArticle;