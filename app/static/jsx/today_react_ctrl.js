/** @jsx React.DOM */
TodayWrapView = React.createClass({
  getInitialState: function () {
    return {
      currentWord: null,
      words: []
    }
  },
  loadWordsFromServer: function () {
    $.ajax({
      url: this.props.todayApiUrl,
      dataType: 'json',
      success: function(data) {
        console.log(data);
        this.props.words = data.words;
        this.setState({ currentWord: data.words[0] });
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.todayApiUrl, status, err.toString());
      }.bind(this)
    });
  },
  componentDidMount: function () {
    this.loadWordsFromServer();
  },
  render: function () {
    if (this.state.currentWord !== null) {
      return (<div>
                <Title name={this.state.currentWord.name}/>
                <BlockWrap word={this.state.currentWord}/>
                <Pager />
              </div>)
    } else {
      return (<div><Title name={'loading...'} /></div>)
    }
  }
});

Title = React.createClass({
  render: function () {
    return (<div className='row'>
              <div className='col-md-12'>
                <h1 className='page-title'>{ this.props.name }</h1>
              </div>
            </div>)
  }
});

BlockWrap = React.createClass({
  render: function () {
    return (<div className='row'>
              <div className='col-md-12'>
                <div className='list-group'>
                  <Explain explain={this.props.word.explain}/>
                  <Example example={this.props.word.example}/>
                </div>
              </div>
            </div>)
  }
})

Explain = React.createClass({
  render: function () {
    var explainMarkup = marked(this.props.explain.toString(), {sanitize: true});
    return (<div className='list-group-item'>
              <h4 className='list-group-item-heading'>{ 'Explaination:' }</h4>
              <p className='list-group-item-text' dangerouslySetInnerHTML={{__html: explainMarkup}}></p>
            </div>)
  }
});

Example = React.createClass({
  render: function () {
    var exampleMarkup = marked(this.props.example.toString(), {sanitize: true});
    return (<div className='list-group-item'>
              <h4 className='list-group-item-heading'>{ 'Examples:' }</h4>
              <p className='list-group-item-text' dangerouslySetInnerHTML={{__html: exampleMarkup}}></p>
            </div>)
  }
});

Pager = React.createClass({
  render: function () {
    return (<div className='row'>
              <div className='col-md-12'>
                <ul className="pager">
                  <li className="previous">
                    <a href="#">Previous</a>
                  </li>
                  <li className="next">
                    <a href="#">Next</a>
                  </li>
                </ul>
              </div>
            </div>)
  }
});

todayReactWrapDom = document.getElementById('todayWrapView');
todayApiUrl = todayReactWrapDom.getAttribute('data-url');
React.render(<TodayWrapView todayApiUrl={todayApiUrl} />, todayReactWrapDom);