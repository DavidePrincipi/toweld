<?php

$view->rejectFlag($view::INSET_FORM | $view::INSET_WRAP);

printf('<iframe class="container-frame" 
                name="nethgui-cockpit1:localhost/system" 
                src="%s" 
                data-ready="1" 
                data-loaded="1"></iframe>', htmlspecialchars(
    "https://"  . $_SERVER['SERVER_NAME'] . ":9090/cockpit/@localhost/system/index.html"
));

$view->includeCss('
html, body, #allWrapper, #pageContent, .primaryContent { width: 100%; height: 100% }

.Controller {
    display: flex;
    align-items: stretch;
    height: 100%;
    width: 100%;
}
iframe.container-frame {
    display: block;
    border:none;
    flex-grow: 1;
}
');
