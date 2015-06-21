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
        console.error(this.props.listApiUrl, status, err.toString());
      }.bind(this)
    });
  },
  componentDidMount: function () {
    this.loadWordsFromServer();
  },
  handleDeleteClickCallback: function (wordID) {
    var results = $.grep(this.props.words, function (word) {
      if (wordID === word.id) {
        return true;
      }

      return false;
    });
    searchText = document.getElementById('searchText').value.trim();

    if (results.length === 1) {
      // Update index words
      var indexProps = this.props.words.indexOf(results[0]);
      var indexState = this.state.words.indexOf(results[0]);
      if (indexProps > -1) {
        this.props.words.splice(indexProps, 1);
      }

      if (indexState > -1) {
        this.state.words.splice(indexState, 1);
        this.setState({ words: this.state.words });
      }
    }
  },
  handleSearchSubmit: function (searchText) {
    if (searchText.length > 0) {
      var results = $.grep(this.props.words, function (word) {
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
        <ListView words={this.state.words} handleDeleteClickCallback={this.handleDeleteClickCallback}/>
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
                        <input className='form-control' type='text' placeholder='Search Word' id='searchText' ref='searchText'/>
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
    var self = this;
    var wordRowNodes = this.props.words.map(function (word) {
      return (
        <WordRowView word={word} handleDeleteClickCallback={self.props.handleDeleteClickCallback}/>
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
  handleDeleteClick: function (e) {
    var self = this;
    e.preventDefault();
    $.ajax({
      url: '/delete/' + this.props.word.id,
      type: 'DELETE',
      success: function(data) {
        self.props.handleDeleteClickCallback(this.props.word.id);
      }.bind(this),
      error: function(xhr, status, err) {
        console.error('delete', status, err.toString());
      }.bind(this)
    });
  },
  render: function () {
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
                <span className="glyphicon-hold"></span>
                <a href='#' className='no-decoration' onClick={this.handleDeleteClick}>
                  <span className="glyphicon glyphicon-trash" aria-hidden="true"></span>
                </a>
              </td>
            </tr>)
  }
});

listReactWrapDom = document.getElementById('listReactWrap');
listApiUrl = listReactWrapDom.getAttribute('data-url');
React.render(<ListWrapView listApiUrl={listApiUrl} dataLoadInterval={dataLoadInterval} />, listReactWrapDom);