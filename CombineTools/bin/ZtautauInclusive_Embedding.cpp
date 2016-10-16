#include <string>
#include <map>
#include <set>
#include <iostream>
#include <utility>
#include <vector>
#include <cstdlib>
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"

using namespace std;

int main() {

	//! [part1]
	// First define the location of the "auxiliaries" directory where we can
	// source the input files containing the datacard shapes
	string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/shapes/TALLINN";

	// Create an empty CombineHarvester instance that will hold all of the
	// datacard configuration and histograms etc.
	ch::CombineHarvester cb;
	typedef vector<pair<int, string>> Categories;
	typedef vector<string> VString;

	// Here we will just define two categories for an 8TeV analysis. Each entry in
	// the vector below specifies a bin name and corresponding bin_id.
	VString chns = {"mm"};
        VString embs = {"_et_EB"};

map<string, VString> bkg_procs;
bkg_procs["mm"] = {"W", "QCD", "ZTT", "TT", "VV", "VBFH125", "GGH125","EWKW"};
map<string, VString> sig_procs;
sig_procs["mm"] = {"ZLLsig"};
//ZLL and ZTT are treated as background in the inclusive cat.

map<string, Categories> cats;
cats["mm_13TeV"] = {
	{9,"mm_inclusive"},
        {10,"mm_0jet_comp"}, {11,"mm_1jet_zpt_loose_comp"},
        {12,"mm_1jet_zpt_medium_comp"},{13,"mm_1jet_zpt_tight_comp"},
        {14,"mm_2jet_cp_comp"}, {15,"mm_vbf_comp"},
        {16,"mm_1bjet_comp"}, {17,"mm_2bjet_comp"}, {18,"mm_MSSM_btag_comp"}};

cout << ">> Creating processes and observations...\n";

for (string era : {"13TeV"}) {
    for (auto chn : chns) {
        cb.AddObservations(
                {"*"}, {"ztt"}, {era}, {chn}, cats[chn+"_"+era]);
        cb.AddProcesses(
                {"*"}, {"ztt"}, {era}, {chn}, bkg_procs[chn], cats[chn+"_"+era], false);
        cb.AddProcesses(
                {"*"}, {"ztt"}, {era}, {chn}, sig_procs[chn], cats[chn+"_"+era], true);
    }
}

//Some of the code for this is in a nested namespace, so
// we'll make some using declarations first to simplify things a bit.
using ch::syst::SystMap;
using ch::syst::era;
using ch::syst::bin_id;
using ch::syst::process;

cb.cp().channel({"mm"}).signals()
.AddSyst(cb, "lumi", "lnN", SystMap<>::init(1.05));
cb.cp().channel({"mm"}).backgrounds()
.AddSyst(cb, "lumi", "lnN", SystMap<>::init(1.05));
cb.cp().channel({"mm"}).process({"ZTT"})
.AddSyst(cb, "DY_norm", "lnN", SystMap<>::init(1.05));
cb.cp().channel({"mm"}).signals()
.AddSyst(cb, "DY_norm", "lnN", SystMap<>::init(1.05));

cb.cp().channel({"mm"}).process({"TT"})
.AddSyst(cb, "ttbar_norm", "lnN", SystMap<>::init(1.10));
cb.cp().channel({"mm"}).process({"VV"})
.AddSyst(cb, "VV_norm", "lnN", SystMap<>::init(1.30));
cb.cp().channel({"mm"}).process({"QCD"})
.AddSyst(cb, "QCD_norm", "lnN", SystMap<>::init(1.10));
cb.cp().channel({"mm"}).process({"W"})
.AddSyst(cb, "W_norm", "lnN", SystMap<>::init(1.10));

cb.cp().channel({"mm"}).signals()
.AddSyst(cb, "eff_m", "lnN", SystMap<>::init(1.06));
cb.cp().channel({"mm"}).process({"TT"})
.AddSyst(cb, "eff_m", "lnN", SystMap<>::init(1.06));

cb.cp().channel({"mm"}).signals()
.AddSyst(cb, "MES", "shape", SystMap<>::init(1.00));
cb.cp().channel({"mm"}).process({"ZTT"})
.AddSyst(cb, "MES", "shape", SystMap<>::init(1.00));
cb.cp().channel({"mm"}).process({"TT"})
.AddSyst(cb, "MES", "shape", SystMap<>::init(1.00));

cb.cp().channel({"mm"}).signals()
.AddSyst(cb, "MRES", "shape", SystMap<>::init(1.00));
cb.cp().channel({"mm"}).signals()
.AddSyst(cb, "eff_btag", "lnN", SystMap<>::init(1.06));
cb.cp().channel({"mm"}).backgrounds()
.AddSyst(cb, "eff_btag", "lnN", SystMap<>::init(1.06));

cb.cp().channel({"mm"}).signals()
.AddSyst(cb, "JEC", "shape", SystMap<>::init(1.00));
cb.cp().channel({"mm"}).backgrounds()
.AddSyst(cb, "JEC", "shape", SystMap<>::init(1.00));
cb.cp().channel({"mm"}).signals()
.AddSyst(cb, "RWeight1", "shape", SystMap<>::init(1.00));

cout << ">> Extracting histograms from input root files...\n";
for (string era : {"13TeV"}) {
    for (string chn : chns) {

        string file = aux_shapes+ "/ztt" + embs[0] + ".input-sm-" + era + ".root";
        cb.cp().channel({chn}).backgrounds().ExtractShapes(
                file, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC");
        cb.cp().channel({chn}).signals().ExtractShapes(
                file, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC");
            }
        }


	auto bbb = ch::BinByBinFactory()
	.SetAddThreshold(0.1)
        .SetMergeThreshold(0.5)
	.SetFixNorm(true);

	bbb.AddBinByBin(cb.cp().backgrounds(), cb);
	bbb.AddBinByBin(cb.cp().signals(), cb);

	// This function modifies every entry to have a standardised bin name of
	// the form: {analysis}_{channel}_{bin_id}_{era}
	// which is commonly used in the htt analyses
	ch::SetStandardBinNames(cb);
	//! [part8]

	//! [part9]
	// First we generate a set of bin names:
	set<string> bins = cb.bin_set();
	// This method will produce a set of unique bin names by considering all
	// Observation, Process and Systematic entries in the CombineHarvester
	// instance.


        for (string chn : chns) {
            string folder = ("output/cards/"+chn+"cards"+embs[0]+"/").c_str();
            boost::filesystem::create_directories(folder);
            boost::filesystem::create_directories(folder + "/common");
            TFile output((folder + "/common/ztt_" + chn + embs[0] +".input_I.root").c_str(),
                    "RECREATE");
            auto bins = cb.cp().channel({chn}).bin_set();
            for (auto b : bins) {
                cout << ">> Writing datacard for bin: " << b << "\r" << flush;
                cb.cp().channel({chn}).bin({b}).WriteDatacard(
                        folder + "/" + b + ".txt", output);
            }
            output.Close();
        }


}
