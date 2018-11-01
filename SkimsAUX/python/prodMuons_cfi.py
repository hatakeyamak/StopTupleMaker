
import FWCore.ParameterSet.Config as cms

prodMuons = cms.EDFilter(
  "prodMuons",
  MuonSource    = cms.InputTag('slimmedMuons'),
  VertexSource  = cms.InputTag('offlineSlimmedPrimaryVertices'),#'goodVertices'),
  metSource     = cms.InputTag('slimmedMETs'),
  PFCandSource  = cms.InputTag('packedPFCandidates'),
  RhoSource     = cms.InputTag('fixedGridRhoFastjetCentralNeutral'),
  EAValues      = cms.vdouble(0.0735, 0.0619, 0.0465, 0.0433, 0.0577),
  EAEtaValues   = cms.vdouble(0.8,    1.3,    2.0,    2.2),         
  MinMuPt       = cms.double(5),
  MaxMuEta      = cms.double(2.4),
  MaxMuD0       = cms.double(0.2),
  MaxMuDz       = cms.double(0.5),
  MaxMuRelIso   = cms.double(0.20),
  MaxMuMiniIso  = cms.double(0.20),
  MinMuNumHit   = cms.double(11),
  DoMuonVeto           = cms.bool(False),
  DoMuonID             = cms.bool(True),
  DoMuonVtxAssociation = cms.bool(True),
  DoMuonIsolation      = cms.int32(2), # 1 for relIso; 2 for miniIso; 0 for nothing
  Debug                = cms.bool(False),
  specialFix    = cms.bool(False),
  badGlobalMuonTaggerSrc = cms.InputTag("badGlobalMuonTagger", "bad"),
  cloneGlobalMuonTaggerSrc = cms.InputTag("cloneGlobalMuonTagger", "bad"),
)
