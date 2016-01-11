import React = require("react");
import ArticleTitle = require("./ArticleTitle");
import SummaryList = require("./SummaryList");
import ArticleToggle = require("./ArticleToggle");

class FeedArticle extends React.Component<any, any>{
    constructor(){
        super();
        this.state = {
            isCollapsed: true
        }
    }
    
    
    onToggleClicked(){
        this.setState({
            isCollapsed: !this.state.isCollapsed
        })
    }
    
    render(){
        const article = this.props.article;
        const summary = this.state.isCollapsed ? <div/> : <SummaryList summary={article.summary}/>;
        return (<section className="article">
            <ArticleToggle onToggleClicked={this.onToggleClicked.bind(this)} isCollapsed={this.state.isCollapsed} />
            <ArticleTitle url={article.url} title={article.title}/>      
            <span className="badge article-summary-count">{article.summary.length}</span>      
            {summary}
            </section>);
    }
}

export = FeedArticle;