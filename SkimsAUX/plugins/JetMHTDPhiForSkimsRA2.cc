
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/Math/interface/deltaPhi.h"


class JetMHTDPhiForSkimsRA2 : public edm::EDFilter {

  public:

    explicit JetMHTDPhiForSkimsRA2(const edm::ParameterSet & iConfig);
    ~JetMHTDPhiForSkimsRA2() {}

  private:

    virtual bool filter(edm::Event & iEvent, const edm::EventSetup & iSetup);
    
    edm::InputTag mhtSrc_, jetSrc_;
    edm::EDGetTokenT<edm::View<reco::MET> > MhtTok_;
    edm::EDGetTokenT<edm::View<reco::Jet> > JetTok_;

};


JetMHTDPhiForSkimsRA2::JetMHTDPhiForSkimsRA2(const edm::ParameterSet & iConfig) {
  mhtSrc_ = iConfig.getParameter<edm::InputTag>("MHTSource");
  jetSrc_ = iConfig.getParameter<edm::InputTag>("JetSource");

  MhtTok_= consumes<edm::View<reco::MET> >(mhtSrc_);
  JetTok_= consumes<edm::View<reco::Jet> >(jetSrc_);

  produces<std::vector<float> >("jetMHTDPhiVec");
  produces<float>("dPhi0");
  produces<float>("dPhi1");
  produces<float>("dPhi2");
}


bool JetMHTDPhiForSkimsRA2::filter(edm::Event & iEvent, const edm::EventSetup & iSetup) {

  // read in the objects
  edm::Handle<edm::View<reco::MET> > mht;
  iEvent.getByToken(MhtTok_, mht);
  edm::Handle<edm::View<reco::Jet> > jets;
  iEvent.getByToken(JetTok_, jets);

  std::unique_ptr<std::vector<float> > jetMHTDPhiVecPtr (new std::vector<float> );

  double dPhi0 = 999., dPhi1 = 999., dPhi2 = 999.;

  if (jets->size() >= 1) dPhi0 = std::abs(reco::deltaPhi((*jets)[0].phi(), (*mht)[0].phi()));
  if (jets->size() >= 2) dPhi1 = std::abs(reco::deltaPhi((*jets)[1].phi(), (*mht)[0].phi()));
  if (jets->size() >= 3) dPhi2 = std::abs(reco::deltaPhi((*jets)[2].phi(), (*mht)[0].phi()));

  jetMHTDPhiVecPtr->push_back(dPhi0); jetMHTDPhiVecPtr->push_back(dPhi1); jetMHTDPhiVecPtr->push_back(dPhi2);

  std::unique_ptr<float> dPhi0_CUT(new float); *dPhi0_CUT = dPhi0;
  std::unique_ptr<float> dPhi1_CUT(new float); *dPhi1_CUT = dPhi1;
  std::unique_ptr<float> dPhi2_CUT(new float); *dPhi2_CUT = dPhi2;

  iEvent.put(std::move(jetMHTDPhiVecPtr), "jetMHTDPhiVec");
  iEvent.put(std::move(dPhi0_CUT), "dPhi0");
  iEvent.put(std::move(dPhi1_CUT), "dPhi1");
  iEvent.put(std::move(dPhi2_CUT), "dPhi2");

  return true;

}


#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(JetMHTDPhiForSkimsRA2);
