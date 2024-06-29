function Main0()
	SN = gg.choice({
		"修改面板",
		"还原面板",
		"退出",
	}, nil, "倍率面板")
	if SN==1 then
		HS9()
	end
	if SN==2 then
		HS666()
	end
	if SN==3 then
		exit()
	end
	FX=false
end

function HS9()
    x = gg.prompt({"伤害倍数(默认200倍)"},{"200"},{number})
    n = x[1]
	gg.clearResults()
	gg.setRanges(32)
	gg.searchNumber("0.0001E;1E::30", gg.TYPE_DOUBLE, false, gg.SIGN_EQUAL, 0, -1, 0)
	gg.refineNumber("1", gg.TYPE_DOUBLE, false, gg.SIGN_EQUAL, 0, -1, 0)
	gg.getResults(100)
	gg.editAll(n, gg.TYPE_DOUBLE)
	gg.clearResults()
	gg.toast("修改成功")
end

function HS666()
    x = gg.prompt({"还原倍数(默认200倍)"},{"200"},{number})
    n = x[1]
	gg.clearResults()
	gg.setRanges(32)
	gg.searchNumber("0.0001E;"..n.."::30", gg.TYPE_DOUBLE, false, gg.SIGN_EQUAL, 0, -1, 0)
	gg.refineNumber(n, gg.TYPE_DOUBLE, false, gg.SIGN_EQUAL, 0, -1, 0)
	gg.getResults(100)
	gg.editAll("1", gg.TYPE_DOUBLE)
	gg.toast("还原成功")
end

function exit()
    gg.alert("退出成功")
	os.exit()
end

gg.clearResults()
Main0()
