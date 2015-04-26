/** @jsx React.DOM */
TodayWrapView = React.createClass({
  getInitialState: function () {
    return {
      currentWord: null,
      pos: 0,
      wordCount: 0,
      words: [],
      isDone: false
    }
  },
  loadWordsFromServer: function () {
    $.ajax({
      url: this.props.todayApiUrl,
      dataType: 'json',
      success: function(data) {
        this.props.words = data.words;
        this.setState({
          currentWord: data.words[this.state.pos],
          wordCount: data.words.length
        });
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
    if (this.state.pos > this.props.words.length) {
      this.setState({ isDone: true });
    } else {
      this.setState({
        pos: this.state.pos,
        currentWord: this.props.words[this.state.pos]
      });
    }
  },
  handlePreviousClickCallback: function () {
    if (this.state.pos > 0) {
      this.state.pos -= 1;
      this.setState({
        pos: this.state.pos,
        currentWord: this.props.words[this.state.pos]
      });
    }
  },
  render: function () {
    // No word for today
    if (this.state.currentWord === undefined) {
      return (<div><Title name={'No word for today'} /></div>)
    }
    if (this.state.currentWord !== null) {
      return (<div>
                <Title name={this.state.currentWord.name}/>
                <BlockWrap word={this.state.currentWord}/>
                <Pager handleNextClickCallback={this.handleNextClickCallback}
                       handlePreviousClickCallback={this.handlePreviousClickCallback}
                       pos={this.state.pos}
                       wordCount={this.state.wordCount} />
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
    return (<a className='list-group-item'>
              <h4 className='list-group-item-heading'>{ 'Explaination:' }</h4>
              <div className='list-group-item-text'>
                <span dangerouslySetInnerHTML={{__html: explainMarkup}} />
              </div>
            </a>)
  }
});

Example = React.createClass({
  render: function () {
    var exampleMarkup = marked(this.props.example.toString(), {sanitize: true});
    return (<a className='list-group-item'>
              <h4 className='list-group-item-heading'>{ 'Examples:' }</h4>
              <div className='list-group-item-text'>
                <span dangerouslySetInnerHTML={{__html: exampleMarkup}} />
              </div>
            </a>)
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
    var style = (this.props.pos / (this.props.wordCount - 1)) * 100;
    style = { width: style.toString() + '%' };
    return (<div className='row'>
              <div className='col-md-12'>
                <div className="progress progress-striped active">
                  <div className="progress-bar" style={style}></div>
                </div>
                <ul className="pager">
                  <li className="previous">
                    <a href="#"
                       onClick={this.handlePreviousClick}
                       className={this.props.pos > 0 ? '' : 'hidden'}
                    >Previous</a>
                  </li>
                  <li><span className='page-count'>{ this.props.pos + '/' + (this.props.wordCount - 1) }</span></li>
                  <li className="next">
                    <a href="#"
                       onClick={this.handleNextClick}
                       className={this.props.pos === this.props.wordCount - 1 ? 'hidden' : ''}
                    >Next</a>
                  </li>
                </ul>
              </div>
            </div>)
  }
});

todayReactWrapDom = document.getElementById('todayWrapView');
todayApiUrl = todayReactWrapDom.getAttribute('data-url');
React.render(<TodayWrapView todayApiUrl={todayApiUrl} />, todayReactWrapDom);