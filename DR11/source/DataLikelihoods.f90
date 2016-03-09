    module DataLikelihoodList
    use likelihood
    use settings
    use CosmologyTypes
    implicit none

    contains

    subroutine SetDataLikelihoods(Ini)
    use HST
    use snovae
    use CMBLikelihoods
    use bao
!JAV
    use BBNp
    use bao_MGS
    use bao_Busca
    use bao_Andreu
    use mpk
    use wigglez
    class(TSettingIni), intent(in) :: Ini

    CosmoSettings%get_sigma8 = Ini%Read_Logical('get_sigma8',.false.)

    call CMBLikelihood_Add(DataLikelihoods, Ini)

    call HSTLikelihood_Add(DataLikelihoods, Ini)

    call SNLikelihood_Add(DataLikelihoods, Ini)

    call MPKLikelihood_Add(DataLikelihoods, Ini)

    if (use_mpk) call WiggleZLikelihood_Add(DataLikelihoods, Ini)

    call BAOLikelihood_Add(DataLikelihoods, Ini)
!JAV
    call BBNLikelihood_Add(DataLikelihoods, Ini)

    call BAO_MGS_Likelihood_Add(DataLikelihoods, Ini)
 
    call BAO_Busca_Likelihood_Add(DataLikelihoods, Ini)

    call BAO_Andreu_Likelihood_Add(DataLikelihoods, Ini)

    CosmoSettings%use_LSS = use_mpk

    end subroutine SetDataLikelihoods


    end module DataLikelihoodList
