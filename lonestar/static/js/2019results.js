
$(function() {
	update();
});

function update() {
  
    var data = { method: "Get2019ResultsInfo" }; 
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var resultiInfourl = $("#resultsShell").data('url');
	console.log(resultiInfourl)
    $.ajax({
        url: resultiInfourl,
        headers: {
            "X-CSRFToken": csrftoken
        },
        data: data,
        cache: true,
        dataType: 'json',
        success: function(res, status) {
            console.log(res)
            if (res["valid"]) {
                console.log(res);
                processNewData(res['data']);
            } else {
                console.error("Error from background results refresh: " + res["error"]);
            }
        },
        error: function(res) {
		    console.error(res); 
        },
        timeout: 3000
    });

}

function processNewData(data) {
	// data is sorted by pace among teams that have completed a leg
    var teamslist = data.teams;
    
    teamsjson = JSON.parse(teamslist);
    console.log(teamsjson);
    var teams = Array();
    teamsjson.forEach(teammodel => {
        team_ = teammodel.fields
        team_['id'] = teammodel['pk']
        teams.push(team_)
    });
    console.log(teams)
    let teamInfo = {
        "-377": {"Name": "Your Pace or Mine?", "Id": "623"},
        "-353": {"Name": "Heard of Turtles?", "Id": "647"},
        "-316": {"Name": "i'm bad at team names", "Id": "684"},
        "-291": {"Name": "Who's Watching the Kids", "Id": "709"},
        "-274": {"Name": "Texas Trek'ers", "Id": "726"},
        "-269": {"Name": "City of La Porte Road Dawgs", "Id": "731"},
        "-233": {"Name": "Dolls 'n Towel Boyz", "Id": "767"},
        "-202": {"Name": "myTeam Triumph Wings of Texas", "Id": "577"},
        "1": {"Name": "HCSS Dozers", "Id": "757"},
        "2": {"Name": "HCSS Pile Drivers", "Id": "758"},
        "3": {"Name": "A Few Good Men", "Id": "773"},
        "5": {"Name": "Planks 5.0", "Id": "713"},
        "6": {"Name": "DOGs", "Id": "580"},
        "7": {"Name": "Facet Seven Fitness Hippies", "Id": "774"},
        "8": {"Name": "Rawhide Roadrunners", "Id": "687"},
        "9": {"Name": "Lost in Texas", "Id": "636"},
        "10": {"Name": "DALLAS DOES HOUSTON", "Id": "584"},
        "11": {"Name": "11 Below", "Id": "666"},
        "12": {"Name": "Silver Bullets", "Id": "586"},
        "18": {"Name": "11 Pink Ladies and An Adam's Apple", "Id": "745"},
        "24": {"Name": "Texan Trots", "Id": "556"},
        "30": {"Name": "The Peeps", "Id": "694"},
        "36": {"Name": "36ers", "Id": "765"},
        "50": {"Name": "50 Shades of Trained", "Id": "711"},
        "69": {"Name": "The Mullets", "Id": "670"},
        "100": {"Name": "Tarahumara Hares", "Id": "795"},
        "101": {"Name": "Zero Dark Thirty", "Id": "794"},
        "102": {"Name": "E.R.C.", "Id": "781"},
        "103": {"Name": "Fast & Furious - Long Dash", "Id": "599"},
        "104": {"Name": "Kung Fu Racing Team", "Id": "626"},
        "106": {"Name": "Hooked n' Horny", "Id": "813"},
        "107": {"Name": "Tarahumara Runners", "Id": "801"},
        "108": {"Name": "Notorious BRC", "Id": "566"},
        "109": {"Name": "Young Guns & Old Goats", "Id": "563"},
        "110": {"Name": "Austin Front Runners - Fast & Fabulous", "Id": "644"},
        "111": {"Name": "Wheezing Tomatoes", "Id": "734"},
        "112": {"Name": "On The Run", "Id": "821"},
        "113": {"Name": "Corsicana Running Club", "Id": "785"},
        "114": {"Name": "Night Heron Running Club", "Id": "743"},
        "115": {"Name": "Don't Stop...Give 'Em Hell", "Id": "560"},
        "116": {"Name": "Spirit of the Pack", "Id": "645"},
        "117": {"Name": "Hooked n' Hornier", "Id": "816"},
        "118": {"Name": "SeXC Horns", "Id": "815"},
        "119": {"Name": "Hooked n' Horniest", "Id": "814"},
        "120": {"Name": "BSA Troop 120", "Id": "728"},
        "121": {"Name": "Tenaris Turtle Team", "Id": "742"},
        "122": {"Name": "Flying Sisters", "Id": "671"},
        "123": {"Name": "The Beer View Mirrors", "Id": "575"},
        "124": {"Name": "MRC You at the Finish!", "Id": "776"},
        "125": {"Name": "Big Strides and Rides", "Id": "562"},
        "126": {"Name": "the Schneider Electric's", "Id": "741"},
        "127": {"Name": "ExtraTIRrestrials", "Id": "766"},
        "128": {"Name": "Striders Across Texas", "Id": "722"},
        "129": {"Name": "Operation Jade Helm", "Id": "763"},
        "130": {"Name": "Witness The Fitness", "Id": "808"},
        "131": {"Name": "Better Than Nothing Runners", "Id": "664"},
        "199": {"Name": "199 Problems", "Id": "595"},
        "200": {"Name": "EY", "Id": "780"},
        "201": {"Name": "Insan8e", "Id": "769"},
        "202": {"Name": "Blood Sweat & BEERS", "Id": "576"},
        "203": {"Name": "The Fast and the Furious", "Id": "668"},
        "204": {"Name": "Austin Front Runners Team Mo-mentum", "Id": "582"},
        "205": {"Name": "Solely CG", "Id": "797"},
        "206": {"Name": "How Texas Was Run", "Id": "573"},
        "207": {"Name": "Beauty, Beast, and the Beer", "Id": "592"},
        "208": {"Name": "Kirksey K.A.Boom", "Id": "581"},
        "209": {"Name": "Rowdy Loafers", "Id": "712"},
        "210": {"Name": "One Time At Van Camp", "Id": "692"},
        "211": {"Name": "Obi-Run KenobiÃ¢â‚¬â„¢s", "Id": "791"},
        "212": {"Name": "Texas Roadrunners", "Id": "732"},
        "213": {"Name": "TEAM KINISI", "Id": "689"},
        "214": {"Name": "Scallywags", "Id": "673"},
        "215": {"Name": "Striders Unleashed", "Id": "567"},
        "216": {"Name": "Laces Out", "Id": "680"},
        "217": {"Name": "12 Hangry Women", "Id": "679"},
        "218": {"Name": "Space Force", "Id": "790"},
        "219": {"Name": "Austin Front Runners - Glitter Done", "Id": "698"},
        "221": {"Name": "Sector / Air Station Corpus Christi", "Id": "817"},
        "222": {"Name": "DallAss Kickers", "Id": "715"},
        "223": {"Name": "Agony of DeFeet", "Id": "570"},
        "224": {"Name": "WWRC", "Id": "700"},
        "225": {"Name": "The Fighting Irish", "Id": "642"},
        "226": {"Name": "Ship of Fools", "Id": "744"},
        "227": {"Name": "Worst. Parade. Ever", "Id": "805"},
        "228": {"Name": "Buck Joggers", "Id": "792"},
        "229": {"Name": "Tarahumaras Too", "Id": "631"},
        "230": {"Name": "Victorious Secret", "Id": "629"},
        "231": {"Name": "The Internationals", "Id": "737"},
        "232": {"Name": "Run and Drink It", "Id": "704"},
        "233": {"Name": "Pulled Pork and Hamstrings", "Id": "735"},
        "234": {"Name": "T Force", "Id": "809"},
        "235": {"Name": "War Eagles III", "Id": "630"},
        "236": {"Name": "Mark Watney Rescue Squad", "Id": "669"},
        "237": {"Name": "Running Down A Dream", "Id": "719"},
        "238": {"Name": "Team Bypass", "Id": "724"},
        "239": {"Name": "Dashing Passion", "Id": "771"},
        "240": {"Name": "Scallywags", "Id": "811"},
        "241": {"Name": "TIRed Sole Mates", "Id": "753"},
        "242": {"Name": "Drinkers With A Running Problem", "Id": "640"},
        "243": {"Name": "Riverwood Longhorns", "Id": "588"},
        "244": {"Name": "Will Run for Tacos ", "Id": "661"},
        "245": {"Name": "The Juggornuts", "Id": "598"},
        "246": {"Name": "Tri-County Dream Team", "Id": "755"},
        "247": {"Name": "CATAPULT ", "Id": "788"},
        "248": {"Name": "Where's Jim?", "Id": "752"},
        "249": {"Name": "Master Panda", "Id": "587"},
        "250": {"Name": "Runnin' Away from Crew", "Id": "810"},
        "251": {"Name": "Vanniversary", "Id": "775"},
        "252": {"Name": "Roaming Gnomes", "Id": "634"},
        "253": {"Name": "Team Taco", "Id": "568"},
        "254": {"Name": "Team Slow Twitch", "Id": "660"},
        "255": {"Name": "The TIRRful Return", "Id": "632"},
        "256": {"Name": "Chrome Hearts", "Id": "697"},
        "257": {"Name": "The Loose Cannons", "Id": "593"},
        "258": {"Name": "F3 Meteor", "Id": "708"},
        "259": {"Name": "Boomtown Babes", "Id": "678"},
        "260": {"Name": "Chafing The Dream ", "Id": "699"},
        "261": {"Name": "Lone Star 12", "Id": "693"},
        "262": {"Name": "Team Whirlpool : Is your Refrigerator Running?", "Id": "779"},
        "263": {"Name": "Threat Level Midnight", "Id": "725"},
        "300": {"Name": "Notorious HRG", "Id": "646"},
        "301": {"Name": "John Jairo & Su Combo", "Id": "786"},
        "302": {"Name": "Riverbat Express", "Id": "733"},
        "303": {"Name": "Remember The A'La Mode!", "Id": "723"},
        "304": {"Name": "Team AH", "Id": "682"},
        "305": {"Name": "Super Hero's In Training", "Id": "703"},
        "306": {"Name": "Running For Pizza", "Id": "739"},
        "307": {"Name": "Round Rock Runners Running Around", "Id": "696"},
        "308": {"Name": "Team Klein", "Id": "736"},
        "309": {"Name": "Sons of Liberty", "Id": "663"},
        "310": {"Name": "Raven Scrapers", "Id": "624"},
        "311": {"Name": "Eat, Drink, Run, Sleep, Repeat", "Id": "718"},
        "312": {"Name": "Running Impaired", "Id": "710"},
        "313": {"Name": "The Holy Rollers", "Id": "800"},
        "314": {"Name": "Who Invited Him?", "Id": "802"},
        "315": {"Name": "Road Runners", "Id": "690"},
        "316": {"Name": "Rainmakers", "Id": "655"},
        "317": {"Name": "Fantastic Flight Crew and a Snowflake ", "Id": "777"},
        "318": {"Name": "Crockett's Rockets", "Id": "574"},
        "319": {"Name": "Running KARCasses", "Id": "654"},
        "320": {"Name": "Worst Pace Scenario", "Id": "804"},
        "321": {"Name": "Lost in Pace", "Id": "762"},
        "322": {"Name": "Team RWB B/CS", "Id": "807"},
        "323": {"Name": "Audubon Companies", "Id": "686"},
        "324": {"Name": "Bacon & Legs", "Id": "672"},
        "325": {"Name": "Distance Divas", "Id": "675"},
        "326": {"Name": "Better at Running Up a Tab", "Id": "701"},
        "327": {"Name": "CBA TIRtles", "Id": "677"},
        "328": {"Name": "Mother Truckers", "Id": "601"},
        "329": {"Name": "MRC Screamin' Memes", "Id": "751"},
        "330": {"Name": "Team RWB Austin", "Id": "793"},
        "400": {"Name": "Texas Freedom Runners", "Id": "656"},
        "401": {"Name": "TIRminators", "Id": "583"},
        "402": {"Name": "Sweatbanded Heathens", "Id": "754"},
        "403": {"Name": "Run Slow. Eat Fast.", "Id": "782"},
        "404": {"Name": "Low Maintenance", "Id": "658"},
        "405": {"Name": "Team Fox 2", "Id": "772"},
        "406": {"Name": "Get Tootha Choppa", "Id": "756"},
        "407": {"Name": "Slow n Lazy", "Id": "578"},
        "408": {"Name": "Tirtoogas", "Id": "665"},
        "409": {"Name": "TEAM USA", "Id": "707"},
        "410": {"Name": "Team Fox 1", "Id": "764"},
        "411": {"Name": "West End Runners", "Id": "760"},
        "412": {"Name": "Hudson Farm Co - The Family Who Runs Together", "Id": "643"},
        "413": {"Name": "Good Vibe Nut Tribe", "Id": "600"},
        "414": {"Name": "Team Rum Cake ", "Id": "717"},
        "415": {"Name": "Jack & the Five Sparrows", "Id": "747"},
        "417": {"Name": "Racing Rattlers", "Id": "721"},
        "418": {"Name": "Undertrained, Overconfident, PUMPED UP KICKS", "Id": "650"},
        "419": {"Name": "Legs Miserables", "Id": "799"},
        "420": {"Name": "Girls Who Love To Run", "Id": "685"},
        "421": {"Name": "Truffle Shuffle", "Id": "572"},
        "422": {"Name": "Run This Town", "Id": "783"},
        "423": {"Name": "Texas Roadkill Search Team", "Id": "676"},
        "425": {"Name": "LBO -Life's Better Outside", "Id": "681"},
        "426": {"Name": "SOTA ARMY", "Id": "714"},
        "427": {"Name": "TEAM RWB SAN ANTONIO", "Id": "727"},
        "428": {"Name": "CW3", "Id": "579"},
        "430": {"Name": "Limpaway Scrape", "Id": "602"},
        "431": {"Name": "Madams of Mayhem", "Id": "759"},
        "432": {"Name": "The Lone (State) Runners", "Id": "635"},
        "433": {"Name": "Crossfit Illuminati", "Id": "639"},
        "434": {"Name": "Things We Do For Tacos", "Id": "778"},
        "435": {"Name": "Fireballs", "Id": "637"},
        "436": {"Name": "Smooth Operators", "Id": "667"},
        "512": {"Name": "Sisters with Blisters", "Id": "662"},
        "555": {"Name": "TIR Admin Team", "Id": "820"},
        "600": {"Name": "Sarah Pool - Solo", "Id": "823"},
        "700": {"Name": "Victor Valenzuela - Solo", "Id": "824"},
        "900": {"Name": "Snowdrop Sole Sisters - Rip & Ellis", "Id": "825"},
        "1029": {"Name": "10:29 to H'town", "Id": "740"},
        "1835": {"Name": "Come-and-Takers", "Id": "806"},
        "1836": {"Name": "Return of the Runaway Scrapers", "Id": "691"},
        "1876": {"Name": "Texas A&M Corps of Cadets", "Id": "798"},
        "2132": {"Name": "KINISI TOO", "Id": "688"},
        "2222": {"Name": "2Slow 2Win 2Dumb 2Quit", "Id": "564"},
        "2472": {"Name": "CATAPULT ", "Id": "789"},
        "4232": {"Name": "Texas Roadkill Search Team II", "Id": "818"},        
    };
    
	// top 1 overall
	var html = teams.length == 0 ? "No teams have completed leg 1 yet." : addResultTable(teamInfo, "Overall", [teams[0]]);
	teams.splice(0,1);
    console.log(html);
    console.log(teams[0]);
    console.log(teams.length);
    
	// top 1 female among remaining teams
	for (let i = 0; i < teams.length; ++i) {
		if (teams[i].Type == "Women") {
			html += addResultTable(teamInfo, "Female", [teams[i]]);
			teams.splice(i,1);
			break;
		}
	}
    
	// top 1 corporate among remaining teams
	for (let i = 0; i < teams.length; ++i) {
		if (teams[i].Classification == "Corporate") {
			html += addResultTable(teamInfo, "Corporate", [teams[i]]);
			teams.splice(i,1);
			break;
		}
	}

	// identify divisions among remaining teams and classify teams into them
	let classes = [];
	let divisions = {};
	let cls = "", typ = "";
	for (let i = 0; i < teams.length; ++i) {
		cls = teams[i].Classification;
		typ = teams[i].Type;
		if (cls in divisions) {
			if (typ in divisions[cls]) {
				divisions[cls][typ].push(i);
			} else {
				divisions[cls][typ] = [i];
				divisions[cls]["Types"].push(typ);
			}
		} else {
			divisions[cls] = {"Types": [typ]};
			divisions[cls][typ] = [i];
			classes.push(cls);
		}
	}
    
	// add division tables sorted by classification,type
	classes.sort();
	let curtypes = [], types = [], divLeaders = [];
	for (let c = 0; c < classes.length; ++c) {
		cls = classes[c];
		curtypes = divisions[cls]["Types"];
		// types.sort();
		types = [];
		if (curtypes.includes("Men")) types.push("Men");
		if (curtypes.includes("Women")) types.push("Women");
		if (curtypes.includes("Mixed")) types.push("Mixed");
		for (let t = 0; t < types.length; ++t) {
			typ = divisions[cls][types[t]];
			divLeaders = [];
			for (let p = 0; p < typ.length; ++p) {
				divLeaders.push(teams[typ[p]]);
			}
			html += addResultTable(teamInfo, (cls+" "+types[t]), divLeaders);
		}
	}

	$("#resultsShell").empty();
	$("#resultsShell").append(html);
}

function timeString(diffMilli) {
    let neg = diffMilli < 0 ? "-" : "";
    diffMilli = Math.abs(diffMilli);
    // var numdays = Math.floor(diffMilli / (1000*60*60*24));
    // diffMilli -= (numdays * (1000*60*60*24));
    var numhours = Math.floor(diffMilli / (1000*60*60));
    diffMilli -= (numhours * (1000*60*60));
    var nummins = Math.floor(diffMilli / (1000*60));
    diffMilli -= (nummins * (1000*60));
    var numsecs = Math.floor(diffMilli / 1000);
    var ret = "";
    // if (numdays > 0) ret += numdays + "d";
    ret += neg + (numhours > 0 ? numhours + ":" : "") + (numhours > 0 && nummins < 10 ? "0" : "") + nummins + ":" + (numsecs < 10 ? "0" : "") + numsecs;
    return ret.trim();
}

function addResultTable(teamInfo, title, dataRows) {
    console.log(teamInfo, title, dataRows)
	let html = `<div class="resultPanel">
		<div class="resultTitle">${title}</div>
		<div class="container" style="padding:0;">`;
	for (let i = 0; i < dataRows.length; ++i) {
		let t = dataRows[i];
        let alt = i%2 == 1 ? " altback" : "";
        console.log(t.TeamNumber)
		html += `<div class="row">
                <div class="col-sm-6 col-md-5">${teamInfo[t.TeamNumber].Name}</div>
                <div class="row col-md-6 col-sm-7">
                    <div>Team ${t.TeamNumber}</div>
                    <div>${t.LastHandoffTime}</div>
                    <div>${t.TotalMiles}mi</div>
                    <div>${this.timeString(t.TotalTimeSecs*1000)}</div>
                    <div>${this.timeString(t.TotalPaceSecs*1000)}/mi</div>
                </div>                
			  </div>`;
	}
    html += `</div>`;
    html += `<div>Click to see all</div>`;
    html += `</div>`;
    return html;
}
