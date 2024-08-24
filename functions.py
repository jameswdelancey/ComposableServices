import json
import subprocess


def index():
    return (
        "text/html",
        200,
        b"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="/bootstrap-1.1.1.min.css">
<!-- <link rel="stylesheet" href="https://sitetransform.github.io/sitetransform.css/dist/sitetransform.min.css"> -->
<!-- <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous"> -->
<script src="/jquery-1.5.2.min.js"></script>
<title>SPA for IE6</title>
<script>
window.onload = function() {
  // Load menu items from the server
    loadMenu();

    // Handle hash changes for navigation
    window.onhashchange = renderPage;
    renderPage(); // Initial render
};

function loadMenu() {
    makeRequest('/menu', function(menuItems) {
        var menu = document.getElementById('menu');
        menu.innerHTML = ''; // Clear existing menu items
        var topbarWrapper = document.createElement('div');
        topbarWrapper.className = 'topbar-wrapper';
        topbarWrapper.style.zIndex = '5';
        
        var topbar = document.createElement('div');
        topbar.className = 'topbar';

        var fill = document.createElement('div');
        fill.className = 'fill';

        var container = document.createElement('div');
        container.style = 'margin-left:10px;margin-right:10px;';
        container.className = 'container';
        
        var h3 = document.createElement('h3');
        var projectLink = document.createElement('a');
        projectLink.href = '#';
        projectLink.textContent = 'Project Name';
        h3.appendChild(projectLink);

        var ul = document.createElement('ul');
        
        container.appendChild(h3);
        container.appendChild(ul);
        fill.appendChild(container);
        topbar.appendChild(fill);
        topbarWrapper.appendChild(topbar);
        menu.appendChild(topbarWrapper);

        for (var key in menuItems) {
            var menuItem = document.createElement('li');
            var link = document.createElement('a');
            link.href = '#' + key;
            link.textContent = menuItems[key];
            menuItem.appendChild(link);
            ul.appendChild(menuItem);
        }
    });
}

function renderPage() {
    var pageId = location.hash.slice(1);
    makeRequest('/page/' + pageId, function(pageData) {
        var content = document.getElementById('content');
        content.innerHTML = pageData;
    });
}

function makeRequest(url, callback) {
    var xhr;
    xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var contentType = xhr.getResponseHeader("Content-Type");
                var response;

                if (contentType.indexOf("application/json") !== -1) {
                    // Handle JSON
                    try {
                        response = JSON.parse(xhr.responseText);
                    } catch (e) {
                        // Handle JSON parsing error if needed
                        response = null;
                    }
                } else if (contentType.indexOf("text/html") !== -1) {
                    // Handle HTML
                    response = xhr.responseText;
                } else if (/^image\//.test(contentType)) {
                    // Handle image
                    response = new Image();
                    response.src = URL.createObjectURL(xhr.response);
                    response.onload = function() {
                        URL.revokeObjectURL(response.src); // Clean up after image load
                    };
                    xhr.responseType = 'blob'; // Set responseType to 'blob' for image data
                } else {
                    // Handle other content types if needed
                    response = xhr.responseText;
                }

                callback(response);
            } else {
                // Handle error if needed
                callback(null);
            }
        }
    };

    xhr.open('GET', url, true);
    xhr.send();
}
</script>
</head>
<body style='padding-top: 40px; padding-left: 10px; padding-right: 10px; position: relative;'>
<div class="row" id="menu">
    <!-- Menu items will be loaded here -->
</div>
<!-- <div class="container-fluid"> -->
<!-- <div class="sidebar"> -->
  <!-- ... -->
<!-- </div> -->
<div id="content">
    <!-- Page content will be loaded here -->
</div>
<!-- </div> -->
</body>
</html>
""",
    )


def menu():
    return (
        "application/json",
        200,
        b"""\
{
    "": "Home",
    "contact": "Contact",
    "cam-drive": "Cam Drive",
    "latest-files": "Latest Files",
    "latest-images": "Latest Images",
    "ping": "TCP Pings",
    "fs_stats": "FileStorage Stats",
    "fs_stats2": "FileStorage Stats 2"
}""",
    )


def about():
    return (
        "text/html",
        200,
        b"""\
<div id="about-us-content">
  <div class="page-header"><h1>About Us</h1></div>
  <p>We are a company that does things.</p>
</div>
""",
    )


def cam_drive2():
    return (
        "text/html",
        200,
        b"""\
<div id="about-us-content">
  <div class="page-header"><h1>Abe lint</h1></div>
  <p>We are a super bad company that does things.</p>
</div>
""",
    )


def index2():
    return "text/html", 200, b""


def contact():
    return "text/html", 200, b"c"


def file_bootstrap():
    with open("bootstrap-1.1.1.min.css", "rb") as f:
        return "text/css", 200, f.read()


def file_jquery():
    with open("jquery-1.5.2.min.js", "rb") as f:
        return "text/javascript", 200, f.read()


def cam_drive():
    try:  # Convert this try/except to a decorator
        ret = subprocess.check_output(
            ["python", "ftpbytes.py"],
            input=json.dumps({"ftpbytes_D:/ftproot": ""}).encode("utf-8"),
        )
    except Exception as e:
        return (
            "text/html",
            200,
            b"<h1>Latest Files per Camera</h1><pre>Error: "
            + str(e).encode("utf-8")
            + b"</pre>",
        )
    return "text/html", 200, b"<h1>Cam Drive / Free space</h1><pre>" + ret + b"</pre>"


def latest_files():
    try:  # Convert this try/except to a decorator
        ret = subprocess.check_output(
            ["python", "latestfile.py"],
            input="\n".join(
                json.dumps(x)
                for x in [
                    {"latestfile_D:/ts_cam0": ""},
                    {"latestfile_D:/ts_cam1": ""},
                    {"latestfile_D:/ts_cam2": ""},
                    {"latestfile_D:/ts_cam3": ""},
                    {"latestfile_D:/ts_cam4": ""},
                    {"latestfile_D:/ts_cam5": ""},
                    {"latestfile_D:/ts_cam6": ""},
                    {"latestfile_D:/ts_cam7": ""},
                ]
            ).encode("utf-8"),
        )
    except Exception as e:
        return (
            "text/html",
            200,
            b"<h1>Latest Files per Camera</h1><pre>Error: "
            + str(e).encode("utf-8")
            + b"</pre>",
        )
    return "text/html", 200, b"<h1>Latest Files per Camera</h1><pre>" + ret + b"</pre>"


def ping():
    try:  # Convert this try/except to a decorator
        ret = subprocess.check_output(
            ["python", "tcppinger.py"],
            input="\n".join(
                json.dumps(x)
                for x in [
                    {"tcpping_10.0.0.242": ""},
                    {"tcpping_10.0.0.243": ""},
                    {"tcpping_10.0.0.244": ""},
                    {"tcpping_10.0.0.245": ""},
                    {"tcpping_10.0.0.246": ""},
                    {"tcpping_10.0.0.240": ""},
                    {"tcpping_10.0.0.241": ""},
                    {"tcpping_10.0.0.247": ""},
                ]
            ).encode("utf-8"),
        )
    except Exception as e:
        return (
            "text/html",
            200,
            b"<h1>Latest Files per Camera</h1><pre>Error: "
            + str(e).encode("utf-8")
            + b"</pre>",
        )
    return "text/html", 200, b"<h1>Latest Files per Camera</h1><pre>" + ret + b"</pre>"


def latest_images():
    try:  # Convert this try/except to a decorator
        ret = subprocess.check_output(
            ["python", "ts2jpg.py"],
            input="\n".join(
                json.dumps(x)
                for x in [
                    {"ts2jpg|D:/ts_cam0|D:/ts_cam0.jpg": ""},
                    {"ts2jpg|D:/ts_cam1|D:/ts_cam1.jpg": ""},
                    {"ts2jpg|D:/ts_cam2|D:/ts_cam2.jpg": ""},
                    {"ts2jpg|D:/ts_cam3|D:/ts_cam3.jpg": ""},
                    {"ts2jpg|D:/ts_cam4|D:/ts_cam4.jpg": ""},
                    {"ts2jpg|D:/ts_cam5|D:/ts_cam5.jpg": ""},
                    {"ts2jpg|D:/ts_cam6|D:/ts_cam6.jpg": ""},
                    {"ts2jpg|D:/ts_cam7|D:/ts_cam7.jpg": ""},
                ]
            ).encode("utf-8"),
        )
    except Exception as e:
        return (
            "text/html",
            200,
            b"<h1>Latest Files per Camera</h1><pre>Error: "
            + str(e).encode("utf-8")
            + b"</pre>",
        )
    output = b"<h1>Latest Files per Camera</h1><pre>" + ret + b"</pre>"
    for i in [
        {"ts2jpg|D:/ts_cam0|D:/ts_cam0.jpg": ""},
        {"ts2jpg|D:/ts_cam1|D:/ts_cam1.jpg": ""},
        {"ts2jpg|D:/ts_cam2|D:/ts_cam2.jpg": ""},
        {"ts2jpg|D:/ts_cam3|D:/ts_cam3.jpg": ""},
        {"ts2jpg|D:/ts_cam4|D:/ts_cam4.jpg": ""},
        {"ts2jpg|D:/ts_cam5|D:/ts_cam5.jpg": ""},
        {"ts2jpg|D:/ts_cam6|D:/ts_cam6.jpg": ""},
        {"ts2jpg|D:/ts_cam7|D:/ts_cam7.jpg": ""},
    ]:
        for k in i:
            if k.startswith("ts2jpg"):
                output += f'<img src="{k.rsplit("|")[-1].replace("D:/", "/img/")}" width="800">'.encode(
                    "utf-8"
                )
    return "text/html", 200, output


def ts_cam0():
    with open("D:/ts_cam0.jpg", "rb") as f:
        return "image/jpeg", 200, f.read()


def ts_cam1():
    with open("D:/ts_cam1.jpg", "rb") as f:
        return "image/jpeg", 200, f.read()


def ts_cam2():
    with open("D:/ts_cam2.jpg", "rb") as f:
        return "image/jpeg", 200, f.read()


def ts_cam3():
    with open("D:/ts_cam3.jpg", "rb") as f:
        return "image/jpeg", 200, f.read()


def ts_cam4():
    with open("D:/ts_cam4.jpg", "rb") as f:
        return "image/jpeg", 200, f.read()


def ts_cam5():
    with open("D:/ts_cam5.jpg", "rb") as f:
        return "image/jpeg", 200, f.read()


def ts_cam6():
    with open("D:/ts_cam6.jpg", "rb") as f:
        return "image/jpeg", 200, f.read()


def ts_cam7():
    with open("D:/ts_cam7.jpg", "rb") as f:
        return "image/jpeg", 200, f.read()


def fs_stats():
    ret = subprocess.check_output(
        "python cat.py E:/new_file_storage/data-source-tree/part* | \
python ppjson2jsonlines.py | \
C:\\msys64\\usr\\bin\\wc -l",
        shell=True,
    ).strip()
    ret2 = subprocess.check_output(
        "python cat.py E:/new_file_storage/data-working-copy/part* | \
python ppjson2jsonlines.py | \
C:\\msys64\\usr\\bin\\wc -l",
        shell=True,
    ).strip()
    dpatches = (
        subprocess.check_output(
            "dir E:\\new_file_storage\\data-source-tree-patches | C:\\msys64\\usr\\bin\\grep gz",
            shell=True,
        )
        .strip()
        .replace(b"\r\n", b"\n")
    )
    fpatches = (
        subprocess.check_output(
            "dir E:\\new_file_storage\\file-storage-dir-tree-patch | C:\\msys64\\usr\\bin\\grep gz",
            shell=True,
        )
        .strip()
        .replace(b"\r\n", b"\n")
    )
    ret3 = subprocess.check_output(
        "python cat.py E:/new_file_storage/file-storage-dir-tree/bs* | \
C:\\msys64\\usr\\bin\\wc -l",
        shell=True,
    ).strip()
    ret4 = subprocess.check_output(
        "python cat.py E:/new_file_storage/file-storage-working-dir/bs* | \
C:\\msys64\\usr\\bin\\wc -l",
        shell=True,
    ).strip()

    return (
        "text/html",
        200,
        b"<h1>File Storage Stats</h1><pre>Lines:\n\ndata-source-tree:"
        + ret
        + b"\ndata-working-copy:"
        + ret2
        + b"\nfile-storage-dir-tree:"
        + ret3
        + b"\nfile-storage-working-dir:"
        + ret4
        + b"\npatches on data / data-source-tree-patches:\n"
        + dpatches
        + b"\n\npatches on file listings / file-storage-dir-tree-patch:\n"
        + fpatches
        + b"\n</pre>",
    )


def fs_stats2():
    ret5 = subprocess.check_output(
        "python cat.py E:/new_file_storage/data-source-tree/part* | \
python ppjson2jsonlines.py | \
python sed.py | \
python exists.py | \
python chks1.py --only-check",
        shell=True,
    ).strip()
    ret6 = subprocess.check_output(
        "python cat.py E:/new_file_storage/data-source-tree/part* | \
python ppjson2jsonlines.py | \
python sed.py | \
python exists.py | \
python chks2.py --only-check",
        shell=True,
    ).strip()

    return (
        "text/html",
        200,
        b"<h1>File Storage Stats 2</h1><pre>Lines:"
        + b"\nnumber of files that need a sha256 check on bsl1:"
        + ret5
        + b"\nnumber of files that need a par2 create or validate bsl1:"
        + ret6
        + b"\n</pre>",
    )
