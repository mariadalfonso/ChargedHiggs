import os,sys,re
from optparse import OptionParser

usage = '''  Draw trigger plots from TagAndProbe Trees.
	     This uses trigger matching and Z->tau tau events.
	     No fit on the Z lineshape so far
	'''

parser = OptionParser(usage=usage)
parser.add_option("-p","--plot" ,dest='plot',type='string',help="PlotDir [Default=%default]",default="plot")

opts,args = parser.parse_args()

sys.argv=[]
import ROOT
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)


fROOT = ROOT.TFile.Open("TagAndProbe.root")
if fROOT == None: print "TagAndProbe.root: no such file"
tree = fROOT.Get("tagprobe")
if tree == None: print "tagprobe: no such tree"

ranges={"ptProbe" : "(250,0,250)",
	"etaProbe": "(200,-2.5,2.5)",
	"m" : "(200,0,500)",
	}

xaxis={"ptProbe" : "p_{T}^{#tau,probe} [GeV]",
	"etaProbe": "#eta^{#tau,probe}",
	"m" : "m_{#tau#tau, tag-probe} [GeV]",
	}


what = {}
what [ "trigger" ] = {'var' : ["ptProbe","etaProbe"] , 'base':"", 'sel':"passTrigger" 	, "yaxis" : "trigger eff" }
what [ "ID" ]      = {'var' : ["ptProbe"]            , 'base':"", 'sel':"passId" 	, "yaxis" : "id eff" }
what [ "IDELE" ]   = {'var' : ["ptProbe"]            , 'base':"", 'sel':"passIdEle" 	, "yaxis" : "id(e) eff" }
what [ "IDMU" ]    = {'var' : ["ptProbe"]            , 'base':"", 'sel':"passIdMu" 	, "yaxis" : "id(#mu) eff" }
what [ "ISO" ]     = {'var' : ["ptProbe","m"]        , 'base':"", 'sel':"passIso"	, "yaxis" : "iso eff" }


for name in what:
    for var in what[name]["var"]:
	c=ROOT.TCanvas("c_"+name+"_"+var,name + " "+var, 800,800)
	c.SetRightMargin(0.05)
	c.SetLeftMargin(0.15)
	c.SetTopMargin(0.05)
	c.SetBottomMargin(0.15)

	v = var + ">>base" + ranges[var]	
	s = "isMC==0"
	if what[name]['base'] != "": s += " && " +  what[name]['base']
	print "Drawing base:",v,"|",s
	tree.Draw( v, s ,"goff")

	v = var + ">>sel" + ranges[var]	
	s = "isMC==0"
	if what[name]['sel'] != "": s += " && " +  what[name]['sel']
	print "Drawing sel:",v,"|",s
	tree.Draw( v, s ,"goff")

	base = ROOT.gDirectory.Get('base')
	sel = ROOT.gDirectory.Get('sel')

	sel . Divide(base)

	sel.Draw("HIST")
	sel.GetXaxis().SetTitle( xaxis[var] )
	sel.GetYaxis().SetTitle( what[name]['yaxis'] )
	sel.GetXaxis().SetTitleOffset(1.3)
	sel.GetYaxis().SetTitleOffset(1.3)
	c.Update()
	raw_input("ok?")

	for ext	 in [ 'pdf','png']:
		c.SaveAs( opts.plot + "/" + "tp_"+ name + "_" + var +"."+ ext ) 

#
#root [1] tagprobe->Draw("ptProbe>>base(1000,0,1000)","isMC==0")
#root [2]  tagprobe->Draw("ptProbe>>tr(1000,0,1000)","isMC==0 && passTrigger")
#root [3]  tr->Divide(base)
#root [4]  tr->Draw()
