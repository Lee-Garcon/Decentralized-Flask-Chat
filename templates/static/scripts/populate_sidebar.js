function populateSidebar() {
  var req = new XMLHttpRequest();
  req.onreadystatechange = () => {
    if (req.readyState == 4 && req.status == 200) {
      let contacts = JSON.stringify(req.responseText);

      for (let entry of contacts) {
        populateSidebar.sidebar.innerHTML += `
        <li class="sidebar-entry${(entry.id == config.sysenv.curr_user ? " sidebar-entry-selected" : "")}">
          <div>
            <a href="/chat/${entry.id}">${entry.name}</a>
          </div>
        </li>
        `;
      }
    }
  }
}

config.sysenv.onload_functions.push( () => {
  populateSidebar.sidebar = document.getElementById('converstation-list');
  populateSidebar();
} );
