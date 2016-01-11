import React = require('react');
import FeedArticle = require('./FeedArticle');

class FeedContainer extends React.Component<any, any>{
    constructor() {
        super();
        this.state = {
            articles: {}
        }
    }
    
    
    componentDidMount(){
        $.ajax("content/feed.json").done((articles: any) => {
            this.setState({
                articles: articles
            });
        });
    }
    
    render(){
        const articles = this.state.articles;
        const hasArticles = articles.length > 0;
        const articleElements = hasArticles ? articles.map((article, idx) => <FeedArticle key={idx} article={article}/>) : <p>No article summaries.</p>;
        return (<div className="articles"><h2>Articles</h2>{articleElements}</div>);
    }
    
}

export = FeedContainer;