
import FWCore.ParameterSet.Config as cms

prodElectrons = cms.EDFilter(
  "prodElectrons",
  VetoElectronID   =cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-veto'),
  LooseElectronID   =cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-loose'),
  MediumElectronID   =cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-medium'),
  TightElectronID   =cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-tight'),
  ElectronSource    = cms.InputTag('slimmedElectrons'),
  ConversionsSource = cms.InputTag("reducedEgamma", "reducedConversions"), #not used for WP VETO
  VertexSource      = cms.InputTag('offlineSlimmedPrimaryVertices'),#goodVertices'),
  metSource         = cms.InputTag('slimmedMETs'),
  PFCandSource = cms.InputTag('packedPFCandidates'),
  BeamSpotSource    = cms.InputTag("offlineBeamSpot"),
  RhoSource     = cms.InputTag('fixedGridRhoFastjetCentralNeutral'),
  MinElePt       = cms.double(5),
  MaxEleEta      = cms.double(2.5),
  MaxEleMiniIso  = cms.double(0.10),
  DoElectronVeto           = cms.bool(False),
  Dod0dz                   = cms.bool(True),
  DoElectronID             = cms.bool(True),
  DoElectronVtxAssociation = cms.bool(True),
  DoElectronIsolation      = cms.int32(2), # 1 for relIso; 2 for miniIso; 0 for nothing
  Debug                    = cms.bool(False)
)
