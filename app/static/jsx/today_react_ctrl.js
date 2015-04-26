/** @jsx React.DOM */
TodayWrapView = React.createClass({
  getInitialState: function () {
    return {
      currentWord: null,
      pos: 0,
      words: []
    }
  },
  loadWordsFromServer: function () {
    $.ajax({
      url: this.props.todayApiUrl,
      dataType: 'json',
      success: function(data) {
        this.props.words = data.words;
        this.setState({ currentWord: data.words[this.state.pos] });
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.todayApiUrl, status, err.toString());
      }.bind(this)
    });
  },
  componentDidMount: function () {
    this.loadWordsFromServer();
  },
  handleNextClickCallback: function () {
    this.state.pos += 1;
    this.setState({
      pos: this.state.pos,
      currentWord: this.props.words[this.state.pos]
    });
  },
  handlePreviousClickCallback: function () {
    this.state.pos -= 1;
    this.setState({
      pos: this.state.pos,
      currentWord: this.props.words[this.state.pos]
    });
  },
  render: function () {
    if (this.state.currentWord === undefined) {
      // No word for today
      return (<div><Title name={'No word for today'} /></div>)
    }
    if (this.state.currentWord !== null) {
      return (<div>
                <Title name={this.state.currentWord.name}/>
                <BlockWrap word={this.state.currentWord}/>
                <Pager handleNextClickCallback={this.handleNextClickCallback}
                       handlePreviousClickCallback={this.handlePreviousClickCallback} />
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
              <div className='list-group-item-text'>
                <span dangerouslySetInnerHTML={{__html: explainMarkup}} />
              </div>
            </div>)
  }
});

Example = React.createClass({
  render: function () {
    var exampleMarkup = marked(this.props.example.toString(), {sanitize: true});
    return (<div className='list-group-item'>
              <h4 className='list-group-item-heading'>{ 'Examples:' }</h4>
              <div className='list-group-item-text'>
                <span dangerouslySetInnerHTML={{__html: exampleMarkup}} />
              </div>
            </div>)
  }
});

Pager = React.createClass({
  handlePreviousClick: function (e) {
    e.preventDefault();
    this.props.handlePreviousClickCallback();
  },
  handleNextClick: function (e) {
    e.preventDefault();
    this.props.handleNextClickCallback();
  },
  render: function () {
    return (<div className='row'>
              <div className='col-md-12'>
                <ul className="pager">
                  <li className="previous">
                    <a href="#" onClick={this.handlePreviousClick}>Previous</a>
                  </li>
                  <li className="next">
                    <a href="#" onClick={this.handleNextClick}>Next</a>
                  </li>
                </ul>
              </div>
            </div>)
  }
});

todayReactWrapDom = document.getElementById('todayWrapView');
todayApiUrl = todayReactWrapDom.getAttribute('data-url');
React.render(<TodayWrapView todayApiUrl={todayApiUrl} />, todayReactWrapDom);