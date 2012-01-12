%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
%setdefault('html', '')
<div class="box">
<p>Add a new task to the ToDo list:</p>
<form action="/todo/new" method="GET">
<input type="text" size="50" maxlength="100" name="task">
<input type="submit" name="save" value="save">
</form>

{{!html}}

<p>The open items are as follows:</p>
<table border="1">
%for row in rows:
  <tr>
    <td><a href="/todo/edit/{{row[0]}}">{{row[1]}}</a></td>
  </tr>
%end
</table>
</div>
%rebase gui/layout.tpl title=title
