#!/usr/bin/env python
#from HttStyles import GetStyleHtt
#from HttStyles import MakeCanvas
import CombineHarvester.CombineTools.plotting as plot
import ROOT
import re
from array import array

def createAxisHists(n,src,xmin=0,xmax=499):
  result = []
  for i in range(0,n):
    res = src.Clone()
    res.Reset()
    res.SetTitle("")
    res.SetName("axis%(i)d"%vars())
    res.SetAxisRange(xmin,xmax)
    res.SetStats(0)
    result.append(res)
  return result
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#files=["ztt_mm.output-sm-13TeV-1jet_zpt_loose.root","ztt_mm.output-sm-13TeV-1jet_zpt_medium.root","ztt_mm.output-sm-13TeV-1jet_zpt_tight.root","ztt_mm.output-sm-13TeV-2jet_cp.root","ztt_mm.output-sm-13TeV-vbf.root","ztt_mm.output-sm-13TeV-1bjet.root","ztt_mm.output-sm-13TeV-2bjet.root", "ztt_mm.output-sm-13TeV-MSSM_btag.root"]
files=["ztt_mm.output-sm-13TeV-0jet.root","ztt_mm.output-sm-13TeV-1jet_zpt_loose.root","ztt_mm.output-sm-13TeV-1jet_zpt_medium.root","ztt_mm.output-sm-13TeV-1jet_zpt_tight.root","ztt_mm.output-sm-13TeV-2jet_cp.root","ztt_mm.output-sm-13TeV-vbf.root","ztt_mm.output-sm-13TeV-1bjet.root","ztt_mm.output-sm-13TeV-2bjet.root", "ztt_mm.output-sm-13TeV-MSSM_btag.root"]
labels=["mm-0jet","mm-1jet_zpt_loose","mm-1jet_zpt_medium","mm-1jet_zpt_tight","mm-2jet_cp","mm-vbf","mm-1bjet","mm-2bjet","mm-MSSM_btag"]
selections=["0jet","1jet_zpt_loose","1jet_zpt_medium","1jet_zpt_tight","2jet_cp","vbf","1bjet","2bjet","MSSM_btag"]
filesin=["../../../auxiliaries/shapes/TALLINN/ztt_mt_EB.input-sm-13TeV.root"]#,"../../../auxiliaries/shapes/TALLINN/ztt_mm_wTauSpinner.input-sm-13TeV.root"]
categories=["fail_prefit","pass_prefit","fail_postfit","pass_postfit"]
tmp=ROOT.TFile(filesin[0],"r")
h = tmp.Get("mm_1jet_zpt_loose").Get("VV")
nbins = h.GetXaxis().GetNbins()
for ibin in range(0,nbins+1):
   h.SetBinContent(ibin,0)
   h.SetBinError(ibin,0)
ncat=4
nch=2
nfiles=9
width=[0.3,0.2]
pos=[3,4]

c2=ROOT.TCanvas()
c2.cd()
plot.ModTDRStyle(r=0.06, l=0.12)
pads=plot.TwoPadSplit(0.29,0.010,0.035)

for f in range (0,nfiles):
   file=ROOT.TFile("../outputs_mt_EB/"+files[f],"r")
   for i in range (0,ncat):

      Data=file.Get(categories[i]).Get("data_obs")
      if(file.Get(categories[i]).GetListOfKeys().Contains("W")):
         W=file.Get(categories[i]).Get("W")
      else:
         W=h.Clone()
      if(file.Get(categories[i]).GetListOfKeys().Contains("QCD")):
         QCD=file.Get(categories[i]).Get("QCD")
      else:
         QCD=h.Clone()
      VV=file.Get(categories[i]).Get("VV")
      TT=file.Get(categories[i]).Get("TT")
      VBF=file.Get(categories[i]).Get("VBFH125")
      if(file.Get(categories[i]).GetListOfKeys().Contains("GGH125")):
         GG=file.Get(categories[i]).Get("GGH125")
      else:
         GG=h.Clone()
      if(file.Get(categories[i]).GetListOfKeys().Contains("EWKW")):
         EWKW=file.Get(categories[i]).Get("EWKW")
      else:
         EWKW=h.Clone()
      if(file.Get(categories[i]).GetListOfKeys().Contains("ZTTsig")):
         ZTT=file.Get(categories[i]).Get("ZTTsig")
      else:
         ZTT=h.Clone()
      if(file.Get(categories[i]).GetListOfKeys().Contains("ZLL")):
         ZLL=file.Get(categories[i]).Get("ZLL")
      else:
         ZLL=h.Clone()
                 
      #histolist = file.Get(categories[i]).GetListOfKeys()
      #iter = histolist.MakeIterator()
      #key = iter.Next()
      #while key:
      #   print key.GetName()
      #   if(key.GetName()=="ZTTsig"):
      #      ZTT=file.Get(categories[i]).Get("ZTTsig")
      #   elif(key.GetName()=="ZTT"):
      #      ZTT=file.Get(categories[i]).Get("ZTT")
      #   if(key.GetName()=="ZLLsig"):
      #      ZLL=file.Get(categories[i]).Get("ZLLsig")
      #   elif(key.GetName()=="ZLL"):
      #      ZLL=file.Get(categories[i]).Get("ZLL")
      #   key = iter.Next()
      TotProc=file.Get(categories[i]).Get("TotalProcs")

      VV.Add(W) #electroweak only
      VV.Add(EWKW) #electroweak only
      VBF.Add(GG)


      QCD.SetFillColor(ROOT.TColor.GetColor(250,202,255))
      QCD.SetLineColor(ROOT.EColor.kBlack)
      VV.SetFillColor(ROOT.TColor.GetColor(222,90,106))
      VV.SetLineColor(ROOT.EColor.kBlack)
      TT.SetFillColor(ROOT.TColor.GetColor(155,152,204))
      TT.SetLineColor(ROOT.EColor.kBlack)
      ZTT.SetFillColor(ROOT.TColor.GetColor(248,206,104))
      ZTT.SetLineColor(ROOT.EColor.kBlack)
      ZLL.SetFillColor(ROOT.TColor.GetColor(100,192,232))
      ZLL.SetLineColor(ROOT.EColor.kBlack)
      VBF.SetFillColor(ROOT.kBlue)
      VBF.SetLineColor(ROOT.EColor.kBlack)
      QCD.SetMarkerSize(0) 
      VV.SetMarkerSize(0) 
      TT.SetMarkerSize(0) 
      ZLL.SetMarkerSize(0) 
      ZTT.SetMarkerSize(0) 
      VBF.SetMarkerSize(0) 
 
      Data.SetMarkerStyle(20)
      Data.SetMarkerSize(1.2)
      Data.SetMarkerColor(ROOT.EColor.kBlack)
      Data.SetLineColor(ROOT.EColor.kBlack)
      Data.SetLineWidth(2)
      TotProc.SetFillColor(ROOT.EColor.kBlack)
      TotProc.SetFillStyle(3002)
      TotProc.SetMarkerSize(0)
      #TotProc.SetFillColor(plot.CreateTransparentColor(12,1))

      stack=ROOT.THStack("stack","stack")
      stack.Add(VBF)
      stack.Add(QCD)
      stack.Add(VV)
      stack.Add(TT)
      stack.Add(ZLL)
      stack.Add(ZTT)

      #setup style related things
      #c2=MakeCanvas(categories[i],categories[i],750,750)
      #c2.cd()
      #pads=plot.TwoPadSplit(0.29,0.005,0.005)
      pads[0].cd()
      TotProc.Draw()
      Data.Draw()
      stack.Draw()
      xmax = 160
      xmin = 0
      TotProc.GetXaxis().SetRangeUser(xmin,xmax)
      Data.GetXaxis().SetRangeUser(xmin,xmax)
      stack.GetXaxis().SetLimits(xmin,xmax)
      #else:
      #xmax = TotProc.GetXaxis().GetXmax()
      #xmin = TotProc.GetXaxis().GetXmin()
      axish = createAxisHists(2,TotProc,xmin,xmax)
      #print " f %d - cat %d - xmin %d - xmax %d " %(f,i,xmin,xmax)
      #print " TotProc - xmin %d - xmax %d " %(TotProc.GetXaxis().GetXmin(),TotProc.GetXaxis().GetXmax())
      #print " Data - xmin %d - xmax %d " %(Data.GetXaxis().GetXmin(),Data.GetXaxis().GetXmax())
      #axish = createAxisHists(2,TotProc,TotProc.GetXaxis().GetXmin(),TotProc.GetXaxis().GetXmax())
      axish[0].GetXaxis().SetTitle("m_{#tau#tau} (GeV)")
      axish[0].GetYaxis().SetTitle("Events")
      axish[1].GetXaxis().SetTitle("Visible di-#tau mass (GeV)")
      axish[1].GetYaxis().SetTitle("Obs/Exp")
      axish[1].GetYaxis().SetNdivisions(4)
      axish[0].GetXaxis().SetTitleSize(0)
      axish[0].GetXaxis().SetLabelSize(0)
      axish[0].GetYaxis().SetTitleOffset(1.2)
      axish[1].GetYaxis().SetTitleOffset(1.2)
      axish[0].SetMaximum(2*TotProc.GetMaximum())
      axish[0].SetMinimum(0.0)
      #print " axis - xmin %d - xmax %d " %(axish[0].GetXaxis().GetXmin(),axish[0].GetXaxis().GetXmax())
      #stack.Draw()
      #stack.GetXaxis().SetLimits(xmin,xmax)
      #Data.GetXaxis().SetLimits(xmin,xmax)
      #print " Data - xmin %d - xmax %d " %(Data.GetXaxis().GetXmin(),Data.GetXaxis().GetXmax())
      #print " TotProc - xmin %d - xmax %d " %(TotProc.GetXaxis().GetXmin(),TotProc.GetXaxis().GetXmax())
      #Data.Draw()
      #TotProc.Draw()
      #stack.Draw()
      axish[0].Draw()

      stack.Draw("hsame")
      Data.Draw("esame")
      TotProc.Draw("e2same")
      axish[0].Draw("axissame")
 
      #legend = plot.PositionedLegend(0.2,0.3,4,0.03) #mumu
      legend = plot.PositionedLegend(0.30,0.30,3,0.03)
      legend.SetTextFont(42)
      legend.SetTextSize(0.025)
      legend.SetFillColor(0)
      legend.AddEntry(ZTT,"Z#rightarrow#tau#tau","f")
      legend.AddEntry(ZLL,"Z#rightarrowll","f")
      legend.AddEntry(TT,"ttbar+jets","f")
      legend.AddEntry(VV,"Electroweak","f")
      legend.AddEntry(QCD,"QCD","f")
      legend.AddEntry(VBF,"SM H#rightarrow#tau#tau, m_{H}=125 GeV","f")
      legend.AddEntry(Data,"Observed","ep")
      legend.AddEntry(TotProc,"Exp. Uncertainty","f")
      legend.Draw("same")
      latex = ROOT.TLatex()
      latex.SetNDC()
      latex.SetTextAngle(0)
      latex.SetTextColor(ROOT.kBlack)
      latex.SetTextSize(0.026)

      #CMS and lumi labels
      plot.FixTopRange(pads[0], plot.GetPadYMax(pads[0]), 0.15)
      plot.DrawCMSLogo(pads[0], 'CMS', 'Preliminary', 11, 0.045, 0.05, 1.0, '', 1.0)
      plot.DrawTitle(pads[0], "2.3 fb^{-1} (13 TeV)", 3);
  
      #add ratio plot
      DataForRatio = Data.Clone()
      DataForRatio.Divide(TotProc)
      ErrForRatio = TotProc.Clone()
      ErrForRatio.Divide(TotProc)
      #DataForRatio.SetFillColor(plot.CreateTransparentColor(12,1))
      DataForRatio.SetFillColor(ROOT.EColor.kBlack)
      pads[1].cd()
      pads[1].SetGrid(1,1)
      axish[1].Draw("axis")
      axish[1].SetMinimum(0.5)
      axish[1].SetMaximum(1.5)
      DataForRatio.SetMarkerSize(1.2)
      DataForRatio.SetMarkerStyle(20)
      DataForRatio.SetMarkerColor(ROOT.EColor.kBlack)
      DataForRatio.Draw("esame")
      ErrForRatio.SetFillStyle(3002)
      ErrForRatio.SetFillColor(ROOT.EColor.kBlack)
      ErrForRatio.SetMarkerSize(0)
      ErrForRatio.Draw("e2same")
  
      pads[0].cd()
      pads[0].GetFrame().Draw("same")
      pads[0].RedrawAxis()
  
      #l1=add_lumi()
      #l1.Draw("same")
      #l2=add_CMS()
      #l2.Draw("same")
  
      c2.SaveAs("mvis_"+labels[f]+"_"+categories[i]+".png")



