#include <memory>
#include <algorithm>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "JetMETCorrections/Objects/interface/JetCorrector.h"

#include "DataFormats/JetReco/interface/BasicJet.h"
#include "DataFormats/JetReco/interface/BasicJetCollection.h"

#include "DataFormats/METReco/interface/MET.h"

#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

#include "TLorentzVector.h"

class prodEventInfo : public edm::EDFilter {

  public:

    explicit prodEventInfo(const edm::ParameterSet & iConfig);
    ~prodEventInfo();

  private:

    virtual bool filter(edm::Event & iEvent, const edm::EventSetup & iSetup);

    edm::InputTag vtxSrc_;
    edm::InputTag puppiSrc_;
    edm::InputTag genSrc_;
    edm::Handle<std::vector< PileupSummaryInfo > >  PupInfo;
    edm::EDGetTokenT< std::vector<reco::Vertex> > VtxTok_;
    edm::EDGetTokenT<std::vector< PileupSummaryInfo > > PuppiTok_;
    edm::EDGetTokenT<GenEventInfoProduct> GenTok_;
    bool debug_;
    bool isData_;
};


prodEventInfo::prodEventInfo(const edm::ParameterSet & iConfig) {
  vtxSrc_      = iConfig.getParameter<edm::InputTag>("vtxSrc");

  debug_       = iConfig.getParameter<bool>("debug");

  isData_      = true;

  genSrc_ = iConfig.getParameter<edm::InputTag>("genSrc");
  puppiSrc_ = iConfig.getParameter<edm::InputTag>("puppiSrc");
  VtxTok_ = consumes< std::vector<reco::Vertex> >(vtxSrc_);
  PuppiTok_ = consumes<std::vector< PileupSummaryInfo > >(puppiSrc_);
  GenTok_ = consumes<GenEventInfoProduct>(genSrc_);

  produces<int>("vtxSize");
  produces<float>("trunpv");
  produces<float>("avgnpv");
  produces<int>("npv");
  produces<int>("nm1");
  produces<int>("n0");
  produces<int>("np1");
  produces<float>("storedWeight");
}


prodEventInfo::~prodEventInfo() {
}


bool prodEventInfo::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {

  if( !iEvent.isRealData() ) isData_ = false;

  edm::Handle< std::vector<reco::Vertex> > vertices;
  iEvent.getByToken(VtxTok_, vertices);
//  reco::Vertex::Point vtxpos = (vertices->size() > 0 ? (*vertices)[0].position() : reco::Vertex::Point());

  std::unique_ptr<int> vtxSize(new int);
  *vtxSize = vertices->size();

  std::unique_ptr<float> tru_npv(new float);
  *tru_npv = -1;

  std::unique_ptr<float> avg_npv(new float);
  *avg_npv = 0;

  std::unique_ptr<int> nm1(new int), n0(new int), np1(new int), npv(new int);
  *nm1 = -1; *n0 = -1; *np1 = -1; *npv = -1;

  std::unique_ptr<float> storedWeight(new float);
  *storedWeight = -1.0;

  if( !isData_ ){
     iEvent.getByToken(PuppiTok_, PupInfo);
     std::vector<PileupSummaryInfo>::const_iterator PVI;

     for(PVI = PupInfo->begin(); PVI != PupInfo->end(); ++PVI) {

        int BX = PVI->getBunchCrossing();

        *avg_npv += double(PVI->getPU_NumInteractions());

        if(BX == -1) {
           *nm1 = PVI->getPU_NumInteractions();
        }
        if(BX == 0) {
           *n0 = PVI->getPU_NumInteractions();
        }
        if(BX == 1) {
           *np1 = PVI->getPU_NumInteractions();
        }

        if(BX == 0) {
           *npv = PVI->getPU_NumInteractions();
           *tru_npv = PVI->getTrueNumInteractions();
           continue; // No touching of this "continue", since I'm not sure why it's here originally
        }
     }
     *avg_npv /= 3.0;

     edm::Handle<GenEventInfoProduct> genEvtInfoHandle;
     iEvent.getByToken(GenTok_, genEvtInfoHandle);
     if (genEvtInfoHandle.isValid()) {
        *storedWeight = genEvtInfoHandle->weight();
     }
  }

  iEvent.put(std::move(vtxSize), "vtxSize");
  iEvent.put(std::move(tru_npv), "trunpv");
  iEvent.put(std::move(avg_npv), "avgnpv");
  iEvent.put(std::move(npv), "npv");
  iEvent.put(std::move(nm1), "nm1");
  iEvent.put(std::move(n0), "n0");
  iEvent.put(std::move(np1), "np1");
  iEvent.put(std::move(storedWeight), "storedWeight");

  return true;
}


#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(prodEventInfo);
