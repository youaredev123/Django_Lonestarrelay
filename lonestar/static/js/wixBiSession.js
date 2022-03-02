var wixBiSession = {
    initialTimestamp: Date.now()
    , ssrRequestTimestamp: 1592614710713
    , requestId: publicModel.requestId
    , genGUID: function () {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,function(c){var r=Math.random()*16|0,v=c=='x'?r:(r&0x3|0x8);return v.toString(16);});
    }
    , sessionId: '70589c53-3c58-4a51-8be7-c7310883d3ad'
    , initialRequestTimestamp: performance.timeOrigin ? performance.timeOrigin : Date.now() - performance.now()
    
    
    , is_rollout: 0
    , isSAVrollout: 0
    , isDACrollout: 0
    , is_platform_loaded: 1
    , suppressbi: false
    , dc: '84'
    , renderType: 'bolt'
    , siteRevision: '2286'
    , siteCacheRevision: '1591993961689'
    , wixBoltExclusionReason: ''
    , wixBoltExclusionReasonMoreInfo: ''
    , checkVisibility: (function () {
        var alwaysVisible = document.hidden !== true;
        function checkVisibility() {
            alwaysVisible = alwaysVisible && document.hidden !== true;
            return alwaysVisible;
        }
        document.addEventListener('visibilitychange', checkVisibility, false);
        return checkVisibility;
    })()
    , cacheCookie: document.cookie.match(/ssr-caching="?cache[,#]\s*desc=(\w+)(?:[,#]\s*varnish=(\w+))?(?:[,#]\s*dc[,#]\s*desc=(\w+))?(?:"|;|$)/)
    , setCaching: function (bodyCacheable) {
        if (!bodyCacheable) {
            wixBiSession.caching = undefined;
        }

        var parts = wixBiSession.cacheCookie;
        if (parts) {
            set(parts);
        }

        if (window.PerformanceServerTiming) {
            var serverTiming = performance.getEntriesByType('navigation')[0].serverTiming;
            if (serverTiming && serverTiming.length) {
                var names = [, 'cache', 'varnish', 'dc'];
                parts = [];
                serverTiming.forEach(function (entry) {
                    var i = names.indexOf(entry.name);
                    if (i > 0) {
                        parts[i] = entry.description;
                    }
                });
                set(parts);
            }
        }

        if (!wixBiSession.caching) {
            wixBiSession.caching = 'none';
            wixBiSession.isCached = false;
        }

        function set(parts) {
            if (bodyCacheable && parts[1]) {
                wixBiSession.caching = parts[1] + ',' + (parts[2] || 'none');
                wixBiSession.isCached = isCached(parts[1]) || isCached(parts[2]);
            }
            if (parts[3]) {
                wixBiSession.microPop = parts[3];
            }
        }
        function isCached(part) {
            return !!part && part.indexOf('hit') === 0;
        }
    }
    , sendBeacon: function (url) {
        if (!wixBiSession.suppressbi) {
        
            var sent = false;
            try {
                sent = navigator.sendBeacon(url);
            } catch (e) {}
            if (!sent) {
                (new Image()).src = url;
            }
        
        }
    }
    , sendBeat: (function () {
        var beatUrl = 'https://frog.wix.com/bt?src=29&evid=3'
            + '&v=1.6107.0'
            + '&msid=b6cc7fe0-2bcf-456a-9d80-49488fbda7d5'
            + '&isp=1'
            + '&st=2'
            + '&dc=84'
            + '&iss=1';
        var prevMark = 'fetchStart';
        return function(et, name, extra, pageNumber) {
            var tts = Math.round(performance.now());
            var ts = et === 1 ? 0 : Date.now() - wixBiSession.initialTimestamp;
            if (name && performance.mark) {
                var mark = name + ' (beat ' + et + ')';
                performance.mark(mark);
                if (performance.measure) {
                    performance.measure('\u2B50' + mark, prevMark, mark);
                }
                prevMark = mark;
            }
            var analytics = true;
            if (window.consentPolicyManager) {
                var pm = consentPolicyManager.getCurrentConsentPolicy();
                if (!pm.policy.essential) {
                    return;
                }
                analytics = pm.policy.analytics && pm.policy.functional;
            }
            extra = (analytics && extra) || '';
            if (extra.indexOf('pn=') === -1) {
                extra += '&pn=' + (pageNumber || '1');
            }
            var url = location.href;
            if (!analytics) {
                url = url.replace(/\?.*$/, '');
            } else {
                var referrer = document.referrer;
                if (referrer) {
                    extra += '&ref=' + encodeURIComponent(referrer);
                }
                var match = document.cookie.match(/_wixCIDX=([^;]*)/)
                if (match) {
                    extra += '&client_id=' + match[1];
                }
                extra += genField('visitorId', 'vid');
                extra += genField('siteMemberId', 'mid');
                if (extra.indexOf('sr=') === -1 && screen.width) {
                    extra += '&sr=' + screen.width + 'x' + screen.height;
                }
                if (screen.availWidth) {
                    extra += '&sar=' + screen.availWidth + 'x' + screen.availHeight;
                }
                if (extra.indexOf('wr=') === -1 && window.innerWidth) {
                    extra += '&wr=' + window.innerWidth + 'x' + window.innerHeight;
                }
                if (window.outerWidth) {
                    extra += '&wor=' + window.outerWidth + 'x' + window.outerHeight;
                }
                if (extra.indexOf('ita=') === -1) {
                    extra += '&ita=' + toBool(wixBiSession.checkVisibility());
                }
            }
            if (wixBiSession.siteRevision || wixBiSession.siteCacheRevision) {
                extra += '&siterev=' + wixBiSession.siteRevision + "-" + wixBiSession.siteCacheRevision;
            }
            if (wixBiSession.hasOwnProperty('isUsingMesh')) {
                extra += '&ism=' + toBool(wixBiSession.isUsingMesh);
            }
            if (wixBiSession.hasOwnProperty('caching')) {
                extra += genField('caching') + '&is_cached=' + toBool(wixBiSession.isCached);
            }
            wixBiSession.sendBeacon(beatUrl
                + '&et=' + et
                + (name ? '&event_name=' + encodeURIComponent(name) : '')
                + '&ts=' + ts
                + '&tts=' + tts
                + '&vsi=' + wixBiSession.viewerSessionId
                + '&rid=' + wixBiSession.requestId
                + '&viewer_name=' + encodeURIComponent(wixBiSession.renderType)
                + '&is_rollout=' + wixBiSession.is_rollout
                + '&is_platform_loaded=' + wixBiSession.is_platform_loaded
                + genField('sessionId')
                + '&url=' + encodeURIComponent(url.replace(/^http(s)?:\/\/(www\.)?/, ''))
                + extra
            );
        };

        function genField(name, label) {
            return wixBiSession[name] ? '&' + (label || name) + '=' + wixBiSession[name] : '';
        }
        function toBool(v) {
            return v ? '1' : '0';
        }
    })()
};
wixBiSession.viewerSessionId = wixBiSession.genGUID();
wixBiSession.setCaching(true);
wixBiSession.sendBeat(1, 'Init');