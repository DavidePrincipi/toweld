<?php

namespace NethServer\Module;

class Cockpit extends \Nethgui\Controller\AbstractController
{
    protected function initializeAttributes(\Nethgui\Module\ModuleAttributesInterface $base)
    {
        return \Nethgui\Module\SimpleModuleAttributesProvider::extendModuleAttributes($base, 'Configuration', 50);
    }
}