
(function( $ ) {

    var service = cockpit.dbus('org.nethserver.toweld1')
    var cdb = service.proxy('org.nethserver.toweld1.Esdb', '/org/nethserver/toweld1/Esdb/configuration');

    cdb.call("GetProp", ['sysconfig', 'ProductName']).done(function(value) {
        $('#toweldout').text(value + ' ');
    });

    cdb.wait(function(){
        cdb.GetProp('sysconfig', 'Version').done(function(value) {
            $('#toweldout').append(value);
        });

    });

}( jQuery ));





