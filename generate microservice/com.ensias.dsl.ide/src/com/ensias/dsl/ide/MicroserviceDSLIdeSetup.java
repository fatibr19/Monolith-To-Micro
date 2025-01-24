/*
 * generated by Xtext 2.37.0
 */
package com.ensias.dsl.ide;

import com.ensias.dsl.MicroserviceDSLRuntimeModule;
import com.ensias.dsl.MicroserviceDSLStandaloneSetup;
import com.google.inject.Guice;
import com.google.inject.Injector;
import org.eclipse.xtext.util.Modules2;

/**
 * Initialization support for running Xtext languages as language servers.
 */
public class MicroserviceDSLIdeSetup extends MicroserviceDSLStandaloneSetup {

	@Override
	public Injector createInjector() {
		return Guice.createInjector(Modules2.mixin(new MicroserviceDSLRuntimeModule(), new MicroserviceDSLIdeModule()));
	}
	
}
