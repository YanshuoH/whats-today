/** @jsx React.DOM */

var ListWrapView = React.createClass({
  getInitialState: function () {
    return {
      words: []
    }
  },
  loadWordsFromServer: function () {
    $.ajax({
      url: this.props.listApiUrl,
      dataType: 'json',
      success: function(data) {
        this.props.words = data.words;
        this.setState({ words: data.words });
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  componentDidMount: function () {
    this.loadWordsFromServer();
    setInterval(this.loadWordsFromServer, this.props.dataLoadInterval);
  },
  handleSearchSubmit: function (searchText) {
    if (searchText.length > 0) {
      var results = $.grep(this.state.words, function (word) {
        var n = word.name.search(new RegExp(searchText, 'i'));
        if (n > -1) {
          return true;
        }

        return false;
      });

      this.setState({ words: results });
    } else {
      this.setState({ words: this.props.words });
    }
  },
  render: function () {
    return (<div>
        <SearchView handleSearchSubmitCallback={this.handleSearchSubmit}/>
        <ListView words={this.state.words}/>
        </div>)
  }
});

var SearchView = React.createClass({
  handleSearchClick: function (e) {
    e.preventDefault();
    var searchText = React.findDOMNode(this.refs.searchText).value.trim();
    this.props.handleSearchSubmitCallback(searchText);
  },
  render: function () {
    return (<div className='row'>
              <div className='col-md-12 well'>
                <div className='form-horizontal no-margin-bottom'>
                  <fieldset>
                    <div className='form-group'>
                      <label className='col-md-2 control-label'>{'Search: '}</label>
                      <div className='col-md-8'>
                        <input className='form-control' type='text' placeholder='Search Word' ref='searchText'/>
                      </div>
                      <div className='col-md-2'>
                        <button className="btn btn-success" onClick={this.handleSearchClick}>{'Submit'}</button>
                      </div>
                    </div>
                  </fieldset>
                </div>
              </div>
            </div>)
  }
});

var ListView = React.createClass({
  render: function () {
    var wordRowNodes = this.props.words.map(function (word) {
      return (
        <WordRowView word={word} />
      );
    });

    return (<div className='row'>
              <div className='col-md-12'>
                <table className='table table-striped table-hover'>
                  <thead>
                    <tr>
                      <td>ID</td>
                      <td>Word</td>
                      <td>Create Date</td>
                      <td>Stage</td>
                      <td>Actions</td>
                    </tr>
                  </thead>
                  <tbody>
                    {wordRowNodes}
                  </tbody>
                </table>
              </div>
            </div>)
  }
}); 

var WordRowView = React.createClass({
  render: function() {
    editUrl = '/edit/' + this.props.word.id
    deleteUrl = '/delete/' + this.props.word.id
    return (<tr>
              <td>{this.props.word.id}</td>
              <td>{this.props.word.name}</td>
              <td>{this.props.word.created_at}</td>
              <td>{1}</td>
              <td>
                <a href={editUrl} className='no-decoration'>
                  <span className="glyphicon glyphicon-pencil" aria-hidden="true"></span>
                </a>
                <a href={editUrl} className='no-decoration'>
                  <span className="glyphicon glyphicon-trash" aria-hidden="true"></span>
                </a>
              </td>
            </tr>)
  }
});

listReactWrapDom = document.getElementById('listReactWrap');
listApiUrl = listReactWrapDom.getAttribute('data-url');
dataLoadInterval = listReactWrapDom.getAttribute('data-load-interval');
React.render(<ListWrapView listApiUrl={listApiUrl} dataLoadInterval={dataLoadInterval} />, listReactWrapDom);