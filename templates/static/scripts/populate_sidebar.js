function populateSidebar() {
  var req = new XMLHttpRequest();
  req.onreadystatechange = () => {
    if (req.readyState == 4 && req.status == 200) {
      let contacts = JSON.stringify(req.responseText);

      for (let entry of contacts) {
        populateSidebar.sidebar.innerHTML += `
        <li class="sidebar-entry${(entry.id == config.sysenv.curr_user ? " sidebar-entry-selected" : "")}">
          <button href="/chat/${entry.id}">
            <p>${entry.name}</p>
          </button>
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
